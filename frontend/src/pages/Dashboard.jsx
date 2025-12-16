import React, { useState, useEffect } from 'react';
import dayjs from 'dayjs';
import { Layout, Menu, Table, Tag, Button, Modal, Form, Input, InputNumber, message, Card, Row, Col, Statistic, Select, Tooltip, TimePicker } from 'antd';
import { LogoutOutlined, ReloadOutlined, PlusOutlined, DeleteOutlined, SettingOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { getWeiboList, getExpiredWeiboList, addWeiboAccount, removeWeiboAccount, getSystemConfig, saveSystemConfig, getExpiredReport, checkAccount, setBatchInterval, testWebhook, updateUserCredentials, getMe, pushSummary } from '../api/endpoints';

const { Header, Content } = Layout;

const Dashboard = () => {
  const navigate = useNavigate();
  const [accounts, setAccounts] = useState([]);
  const [expiredAccounts, setExpiredAccounts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [isCookieModalVisible, setIsCookieModalVisible] = useState(false);
  const [cookieValue, setCookieValue] = useState('');
  const [form] = Form.useForm();
  const [expiredReport, setExpiredReport] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  const [lastRefreshTime, setLastRefreshTime] = useState(null);
  const [failedUIDs, setFailedUIDs] = useState([]);
  const [progress, setProgress] = useState({}); // { uid: { status: '等待中'|'进行中'|'完成'|'失败', reason?: string } }
  const [expiredDays, setExpiredDays] = useState(1);
  const [isWebhookModalVisible, setIsWebhookModalVisible] = useState(false);
  const [webhookValue, setWebhookValue] = useState('');
  const [isIntervalModalVisible, setIsIntervalModalVisible] = useState(false);
  const [intervalHours, setIntervalHours] = useState(1);
  const [webhookDailyTime, setWebhookDailyTime] = useState(null);
  const [expiredDaysInput, setExpiredDaysInput] = useState(1);
  const [isAccountModalVisible, setIsAccountModalVisible] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [currentUsername, setCurrentUsername] = useState('');
  const getTokenSub = () => {
    try {
      const t = localStorage.getItem('token');
      if (!t) return '';
      const parts = t.split('.');
      if (parts.length !== 3) return '';
      const payload = JSON.parse(atob(parts[1]));
      return payload.sub || '';
    } catch {
      return '';
    }
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      let daysCfg = 1;
      try {
        const cfg = await getSystemConfig('expired_days');
        if (cfg?.data?.value) daysCfg = Number(cfg.data.value) || 3;
      } catch (e) {}
      setExpiredDays(daysCfg);
      const [listRes, expiredRes, reportRes] = await Promise.all([
        getWeiboList(),
        getExpiredWeiboList(daysCfg),
        getExpiredReport(daysCfg)
      ]);
      setAccounts(listRes.data);
      setExpiredAccounts(expiredRes.data);
      setExpiredReport(reportRes.data);
    } catch (error) {
      console.error(error);
      message.error('获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60000); // Auto refresh every minute
    return () => clearInterval(interval);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleAdd = async (values) => {
    try {
      await addWeiboAccount(values.uid, values.screen_name, values.check_interval);
      message.success('添加成功');
      setIsModalVisible(false);
      form.resetFields();
      fetchData();
    } catch (error) {
      message.error('添加失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleDelete = async (id) => {
    try {
      await removeWeiboAccount(id);
      message.success('删除成功');
      fetchData();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleCheck = async (uid) => {
    try {
      await checkAccount(uid);
      message.success('检查完成');
      fetchData();
    } catch (error) {
      message.error('检查失败');
    }
  };

  const handleFullRefresh = async () => {
    setRefreshing(true);
    setFailedUIDs([]);
    try {
      try {
        const me = await getMe();
        setCurrentUsername(me.data.username || '');
      } catch {}
      const listRes = await getWeiboList();
      const list = listRes.data || [];
      const init = {};
      list.forEach(item => { init[item.uid] = { status: '等待中' }; });
      setProgress(init);
      const failed = [];
      for (const item of list) {
        setProgress(prev => ({ ...prev, [item.uid]: { status: '进行中' } }));
        try {
          const res = await checkAccount(item.uid);
          const reason = res?.data?.message ? String(res.data.message) : '';
          
          // Update local state immediately
          setAccounts(prev => prev.map(acc => {
            if (acc.uid === item.uid) {
                return {
                    ...acc,
                    last_update_time: res.data.last_update_time || acc.last_update_time,
                    last_check_time: new Date().toISOString(),
                    status: res.data.last_update_time ? 'normal' : acc.status
                };
            }
            return acc;
          }));

          setProgress(prev => ({ ...prev, [item.uid]: { status: '完成', reason } }));
        } catch (e) {
          const reason = e?.response?.data?.detail ? String(e.response.data.detail) : (e?.message ? String(e.message) : '未知错误');
          setProgress(prev => ({ ...prev, [item.uid]: { status: '失败', reason } }));
          failed.push(item.uid);
        }
        await new Promise(r => setTimeout(r, 5000));
      }
      setFailedUIDs(failed);
      setLastRefreshTime(new Date());
      await fetchData();
      try {
        await pushSummary(expiredDays);
        message.success('监测结果已汇总推送');
      } catch {}
      if (failed.length > 0) message.error(`部分账号检查失败：${failed.join(', ')}`);
      else message.success('全部账号检查完成');
    } catch (e) {
      message.error('刷新失败');
    } finally {
      setRefreshing(false);
    }
  };

  const handleRetryFailures = async () => {
    if (failedUIDs.length === 0) return;
    setRefreshing(true);
    try {
      const results = await Promise.allSettled(failedUIDs.map(uid => checkAccount(uid)));
      const stillFailed = [];
      results.forEach((r, idx) => { if (r.status === 'rejected') stillFailed.push(failedUIDs[idx]); });
      setFailedUIDs(stillFailed);
      await fetchData();
      if (stillFailed.length > 0) message.error(`仍有失败：${stillFailed.join(', ')}`);
      else message.success('失败账号已重试完成');
    } catch (e) {
      message.error('重试失败');
    } finally {
      setRefreshing(false);
    }
  };


  const handleOpenCookieModal = async () => {
    try {
        const res = await getSystemConfig('weibo_cookie');
        setCookieValue(res.data.value || '');
    } catch (error) {
        // Ignore 404 or other errors
        setCookieValue('');
    }
    setIsCookieModalVisible(true);
  };

  const handleSaveCookie = async () => {
    try {
        await saveSystemConfig('weibo_cookie', cookieValue, 'Weibo Crawler Cookie');
        message.success('Cookie 配置保存成功');
        setIsCookieModalVisible(false);
    } catch (error) {
        message.error('保存失败');
    }
  };

  const handleOpenWebhookModal = async () => {
    try {
      const res = await getSystemConfig('webhook_url');
      setWebhookValue(res.data.value || '');
    } catch (error) {
      setWebhookValue('');
    }
    try {
      const t = await getSystemConfig('webhook_daily_time');
      setWebhookDailyTime(t.data.value || null);
    } catch {}
    try {
      const d = await getSystemConfig('expired_days');
      setExpiredDaysInput(d.data.value ? Number(d.data.value) : expiredDays);
    } catch { setExpiredDaysInput(expiredDays); }
    setIsWebhookModalVisible(true);
  };

  const handleSaveWebhook = async () => {
    try {
      await saveSystemConfig('webhook_url', webhookValue, 'Webhook URL');
      if (webhookDailyTime)
        await saveSystemConfig('webhook_daily_time', webhookDailyTime, '每日推送时间');
      if (expiredDaysInput)
        await saveSystemConfig('expired_days', String(expiredDaysInput), '提醒阈值(天)');
      setExpiredDays(expiredDaysInput);
      message.success('Webhook 已保存');
      setIsWebhookModalVisible(false);
      fetchData();
    } catch (error) {
      message.error('保存失败');
    }
  };

  const handleTestWebhook = async () => {
    try {
      await testWebhook();
      message.success('测试推送已发送');
    } catch {
      message.error('测试推送失败');
    }
  };

  const handleOpenIntervalModal = () => {
    setIsIntervalModalVisible(true);
  };

  const handleSaveInterval = async () => {
    try {
      const seconds = intervalHours * 3600;
      await setBatchInterval(seconds);
      message.success('检查间隔已批量设置');
      setIsIntervalModalVisible(false);
      fetchData();
    } catch (error) {
      message.error('设置失败');
    }
  };

  const computeStatusLabel = (record) => {
    const thresholdDays = expiredDays;
    let isOverdue = false;
    if (!record.last_update_time) {
      isOverdue = true;
    } else {
      const updateDate = dayjs(record.last_update_time).startOf('day');
      const checkDate = record.last_check_time ? dayjs(record.last_check_time).startOf('day') : dayjs().startOf('day');
      const diffDays = checkDate.diff(updateDate, 'day');
      isOverdue = diffDays >= thresholdDays;
    }
    if (isOverdue) return '异常';
    let label = '正常';
    if (record.status === 'error') label = '异常';
    if (record.status === 'expired') label = '已过期';
    return label;
  };

  const formatDateText = (text) => text ? new Date(text).toLocaleString('zh-CN', { hour12: false, timeZone: 'Asia/Shanghai' }) : '';

  const escapeCSV = (v) => {
    if (v === undefined || v === null) return '';
    const s = String(v).replace(/"/g, '""');
    return /[",\n]/.test(s) ? `"${s}"` : s;
  };

  const rowsToCSV = (rows) => {
    const headers = ['UID', '昵称', '状态', '最后更新时间', '上次检查时间', '检查进度'];
    const lines = rows.map(r => {
      const p = progress[r.uid]?.status || '等待中';
      return [
        escapeCSV(r.uid),
        escapeCSV(r.screen_name),
        escapeCSV(computeStatusLabel(r)),
        escapeCSV(formatDateText(r.last_update_time)),
        escapeCSV(formatDateText(r.last_check_time)),
        escapeCSV(p),
      ].join(',');
    });
    return [headers.join(','), ...lines].join('\n');
  };

  const downloadCSV = (filename, csv) => {
    const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleExportList = () => {
    try {
      const csv = rowsToCSV(accounts);
      const filename = `微博监控列表_${dayjs().format('YYYYMMDD_HHmmss')}.csv`;
      downloadCSV(filename, csv);
      message.success('导出成功');
    } catch (e) {
      message.error('导出失败');
    }
  };

  const columns = [
    {
      title: 'UID',
      dataIndex: 'uid',
      key: 'uid',
    },
    {
      title: '昵称',
      dataIndex: 'screen_name',
      key: 'screen_name',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (_, record) => {
        const thresholdDays = expiredDays;
        let isOverdue = false;
        let tip = '';
        if (!record.last_update_time) {
          isOverdue = true;
          tip = '未获取到最后更新时间';
        } else {
          const updateDate = dayjs(record.last_update_time).startOf('day');
          const checkDate = record.last_check_time ? dayjs(record.last_check_time).startOf('day') : dayjs().startOf('day');
          const diffDays = checkDate.diff(updateDate, 'day');
          isOverdue = diffDays >= thresholdDays;
          if (isOverdue) tip = `超过${diffDays}天未更新`;
        }
        if (isOverdue) return <Tooltip title={tip}><Tag color="red">异常</Tag></Tooltip>;
        let color = 'green';
        let label = '正常';
        if (record.status === 'error') { color = 'red'; label = '异常'; }
        if (record.status === 'expired') { color = 'orange'; label = '已过期'; }
        return <Tooltip title={label}><Tag color={color}>{label}</Tag></Tooltip>;
      },
    },
    {
      title: '最后更新时间',
      dataIndex: 'last_update_time',
      key: 'last_update_time',
      render: (text) => text ? new Date(text).toLocaleString('zh-CN', { hour12: false, timeZone: 'Asia/Shanghai' }) : 'N/A',
    },
    {
      title: '上次检查时间',
      dataIndex: 'last_check_time',
      key: 'last_check_time',
      responsive: ['md'],
      render: (text) => text ? new Date(text).toLocaleString('zh-CN', { hour12: false, timeZone: 'Asia/Shanghai' }) : 'N/A',
    },
    {
      title: '检查进度',
      key: 'progress',
      render: (_, record) => {
        const p = progress[record.uid] || { status: '等待中' };
        const s = p.status;
        const colorMap = { '等待中': 'default', '进行中': 'geekblue', '完成': 'green', '失败': 'red' };
        return <Tooltip title={p.reason || s}><Tag color={colorMap[s]}>{s}</Tag></Tooltip>;
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <div>
          <Button type="link" onClick={() => handleCheck(record.uid)}>检查</Button>
          <Button type="link" danger icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)}>删除</Button>
        </div>
      ),
    },
  ];

  return (
    <Layout className="layout" style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0 20px' }}>
        <div style={{ color: 'white', fontSize: '20px', fontWeight: 'bold' }}>微博更新监控系统</div>
        <Button type="primary" icon={<LogoutOutlined />} onClick={handleLogout}>退出登录</Button>
      </Header>
      <Content style={{ padding: '20px' }}>
        <div style={{ background: '#fff', padding: 24, minHeight: 280, borderRadius: 8 }}>
          
          <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
            <Col xs={24} sm={8}>
              <Card>
                <Statistic title="监控账号总数" value={accounts.length} />
              </Card>
            </Col>
            <Col xs={24} sm={8}>
              <Card>
                <Statistic title="超过1天未更新" value={expiredAccounts.length} styles={{ content: { color: '#cf1322' } }} />
              </Card>
            </Col>
            <Col xs={24} sm={8}>
              <Card>
                <Statistic title="正常运行" value={accounts.length - expiredAccounts.length} styles={{ content: { color: '#3f8600' } }} />
              </Card>
            </Col>
          </Row>

          <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
            <div>
              <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalVisible(true)}>
                添加账号
              </Button>
              <Button icon={<SettingOutlined />} onClick={handleOpenCookieModal} style={{ marginLeft: 8 }}>
                配置 Cookie
              </Button>
              <Button onClick={handleOpenWebhookModal} style={{ marginLeft: 8 }}>
                配置 Webhook
              </Button>
              <Button onClick={handleOpenIntervalModal} style={{ marginLeft: 8 }}>
                批量设置检查间隔
              </Button>
              <Button onClick={async () => {
                try {
                  const me = await getMe();
                  setCurrentUsername(me.data.username || '');
                } catch {
                  const sub = getTokenSub();
                  if (sub) setCurrentUsername(sub);
                  else message.error('获取当前用户失败');
                }
                setIsAccountModalVisible(true);
              }} style={{ marginLeft: 8 }}>
                修改账户
              </Button>
            </div>
            <div>
              <Button icon={<ReloadOutlined />} onClick={handleFullRefresh} loading={loading || refreshing}>
                刷新
              </Button>
              <Button style={{ marginLeft: 8 }} onClick={handleExportList}>导出列表</Button>
              {failedUIDs.length > 0 && (
                <Button style={{ marginLeft: 8 }} onClick={handleRetryFailures} loading={refreshing}>重试失败项</Button>
              )}
            </div>
          </div>

          <Table 
            columns={columns} 
            dataSource={accounts} 
            rowKey="id" 
            loading={loading}
            scroll={{ x: 'max-content' }}
            rowClassName={(record) => {
                // Highlight expired accounts if they are in the expired list
                const isExpired = expiredAccounts.find(a => a.id === record.id);
                return isExpired ? 'expired-row' : '';
            }}
          />

          <div style={{ marginTop: 16, background:'#fff1f0', border:'1px solid #ffa39e', borderRadius:8, padding:16 }}>
            <div style={{ fontWeight: 700, marginBottom: 12, color:'#cf1322', display:'flex', alignItems:'center', justifyContent: 'space-between' }}>
              <div style={{ display:'flex', alignItems:'center' }}>
                <ExclamationCircleOutlined style={{ marginRight:8 }} />
                超期未更新提醒
              </div>
              <Button size="small" type="primary" danger onClick={async () => {
                try {
                  await pushSummary(expiredDays);
                  message.success('汇总信息已推送');
                } catch (e) {
                  message.error('推送失败');
                }
              }}>推送汇总</Button>
            </div>
            {expiredAccounts.length === 0 ? (
              <div style={{ color: '#999' }}>暂无超期提醒</div>
            ) : (
              expiredAccounts.map(a => {
                const days = a.last_update_time ? dayjs().startOf('day').diff(dayjs(a.last_update_time).startOf('day'), 'day') : expiredDays;
                return (
                  <div key={a.id} style={{ marginBottom:8, display:'flex', alignItems:'center' }}>
                    <ExclamationCircleOutlined style={{ color:'#cf1322', marginRight:8 }} />
                    <span style={{ marginRight:8 }}>{a.screen_name}</span>
                    <Tag color="red">已超过{days}天</Tag>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </Content>

      <Modal
        title="添加监控账号"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        onOk={form.submit}
      >
        <Form form={form} onFinish={handleAdd} layout="vertical">
          <Form.Item name="uid" label="微博 UID" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="screen_name" label="昵称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="check_interval" label="检查间隔(秒)" initialValue={3600}>
            <InputNumber min={30} style={{ width: '100%' }} />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="配置微博 Cookie"
        open={isCookieModalVisible}
        onCancel={() => setIsCookieModalVisible(false)}
        onOk={handleSaveCookie}
      >
        <p>请输入微博网页版 Cookie (用于获取更精确的更新时间):</p>
        <p style={{ fontSize: '12px', color: '#888' }}>
          提示：登录 weibo.com，打开开发者工具(F12) → 网络(Network) → 刷新页面 → 找到任意请求 → 复制请求头中的 Cookie 值。
        </p>
        <Input.TextArea 
            rows={6} 
            value={cookieValue} 
            onChange={(e) => setCookieValue(e.target.value)} 
            placeholder="SUB=..."
        />
      </Modal>

      <Modal
        title="配置 Webhook"
        open={isWebhookModalVisible}
        onCancel={() => setIsWebhookModalVisible(false)}
        onOk={handleSaveWebhook}
      >
        <Input value={webhookValue} onChange={(e) => setWebhookValue(e.target.value)} placeholder="https://oapi.dingtalk.com/robot/send?access_token=..." />
        <div style={{ marginTop: 12 }}>每日推送时间</div>
        <TimePicker style={{ width: '100%' }} value={webhookDailyTime ? dayjs(webhookDailyTime, 'HH:mm') : null} onChange={(v) => setWebhookDailyTime(v ? v.format('HH:mm') : null)} format="HH:mm" />
        <div style={{ marginTop: 12 }}>提醒阈值(天)</div>
        <InputNumber min={1} value={expiredDaysInput} onChange={(v) => setExpiredDaysInput(v || 1)} style={{ width: '100%' }} />
        <div style={{ marginTop: 12, textAlign: 'right' }}>
          <Button onClick={handleTestWebhook}>推送测试</Button>
        </div>
      </Modal>

      <Modal
        title="修改账户"
        open={isAccountModalVisible}
        onCancel={() => setIsAccountModalVisible(false)}
        onOk={async () => {
          try {
            if (!currentPassword) { message.error('请输入当前密码'); return; }
            if (!newPassword) { message.error('请填写新密码'); return; }
            if (newPassword && newPassword.length < 6) { message.error('新密码至少6位'); return; }
            await updateUserCredentials(currentPassword, undefined, newPassword || undefined);
            message.success('修改成功，请重新登录');
            setIsAccountModalVisible(false);
            localStorage.removeItem('token');
            navigate('/login');
          } catch (e) {
            message.error(e.response?.data?.detail || '修改失败');
          }
        }}
      >
        <Form layout="vertical">
          <Form.Item label="当前用户名">
            <Input value={currentUsername} disabled />
          </Form.Item>
          <Form.Item label="当前密码" required>
            <Input.Password value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} />
          </Form.Item>
          <Form.Item label="新密码">
            <Input.Password value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="批量设置检查间隔"
        open={isIntervalModalVisible}
        onCancel={() => setIsIntervalModalVisible(false)}
        onOk={handleSaveInterval}
      >
        <Select value={intervalHours} onChange={setIntervalHours} style={{ width: '100%' }}
          options={[1,2,3,4,5,6].map(h => ({ value: h, label: `${h} 小时` }))}
        />
      </Modal>


      <style>{`
        .expired-row {
          background-color: #fff1f0;
        }
      `}</style>
    </Layout>
  );
};

export default Dashboard;
