/*
 Navicat Premium Dump SQL

 Source Server         : 222.184.49.22_3307
 Source Server Type    : MySQL
 Source Server Version : 80405 (8.4.5)
 Source Host           : 222.184.49.22:3307
 Source Schema         : weibopyjiank

 Target Server Type    : MySQL
 Target Server Version : 80405 (8.4.5)
 File Encoding         : 65001

 Date: 02/12/2025 10:11:07
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for crawl_logs
-- ----------------------------
DROP TABLE IF EXISTS `crawl_logs`;
CREATE TABLE `crawl_logs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `account_id` int NULL DEFAULT NULL,
  `timestamp` datetime NULL DEFAULT NULL,
  `status` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `account_id`(`account_id` ASC) USING BTREE,
  INDEX `ix_crawl_logs_id`(`id` ASC) USING BTREE,
  CONSTRAINT `crawl_logs_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `weibo_accounts` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 155 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of crawl_logs
-- ----------------------------
INSERT INTO `crawl_logs` VALUES (1, 2, '2025-11-27 20:42:24', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (2, 4, '2025-11-27 20:42:56', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (3, 5, '2025-11-27 20:43:29', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (4, 6, '2025-11-27 20:44:03', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (5, 7, '2025-11-27 20:44:35', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (6, 8, '2025-11-27 20:45:08', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (7, 9, '2025-11-27 20:45:41', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (8, 10, '2025-11-27 20:46:13', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (9, 11, '2025-11-27 20:46:47', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (10, 12, '2025-11-27 20:47:19', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (11, 13, '2025-11-27 20:47:51', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (12, 14, '2025-11-27 20:48:23', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (13, 15, '2025-11-27 20:48:55', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (14, 16, '2025-11-27 20:49:29', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (15, 17, '2025-11-27 20:50:01', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (16, 18, '2025-11-27 20:50:34', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (17, 2, '2025-11-28 08:12:24', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (18, 4, '2025-11-28 08:12:57', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (19, 5, '2025-11-28 08:13:28', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (20, 6, '2025-11-28 08:14:00', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (21, 7, '2025-11-28 08:14:33', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (22, 8, '2025-11-28 08:15:06', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (23, 9, '2025-11-28 08:15:38', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (24, 10, '2025-11-28 08:16:12', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (25, 11, '2025-11-28 08:16:44', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (26, 12, '2025-11-28 08:17:16', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (27, 13, '2025-11-28 08:17:49', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (28, 14, '2025-11-28 08:18:23', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (29, 15, '2025-11-28 08:18:54', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (30, 16, '2025-11-28 08:19:28', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (31, 17, '2025-11-28 08:20:01', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (32, 18, '2025-11-28 08:20:33', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (33, 2, '2025-11-28 19:42:23', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (34, 4, '2025-11-28 19:42:56', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (35, 5, '2025-11-28 19:43:29', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (36, 6, '2025-11-28 19:44:03', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (37, 7, '2025-11-28 19:44:36', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (38, 8, '2025-11-28 19:45:08', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (39, 9, '2025-11-28 19:45:41', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (40, 10, '2025-11-28 19:46:15', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (41, 11, '2025-11-28 19:46:48', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (42, 12, '2025-11-28 19:47:20', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (43, 13, '2025-11-28 19:47:54', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (44, 14, '2025-11-28 19:48:26', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (45, 15, '2025-11-28 19:48:58', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (46, 16, '2025-11-28 19:49:31', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (47, 17, '2025-11-28 19:50:03', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (48, 18, '2025-11-28 19:50:36', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (49, 2, '2025-11-29 07:12:25', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (50, 4, '2025-11-29 07:12:57', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (51, 5, '2025-11-29 07:13:29', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (52, 6, '2025-11-29 07:14:03', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (53, 7, '2025-11-29 07:14:36', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (54, 8, '2025-11-29 07:15:08', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (55, 9, '2025-11-29 07:15:42', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (56, 10, '2025-11-29 07:16:15', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (57, 11, '2025-11-29 07:16:47', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (58, 12, '2025-11-29 07:17:19', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (59, 13, '2025-11-29 07:17:51', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (60, 14, '2025-11-29 07:18:23', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (61, 15, '2025-11-29 07:18:56', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (62, 16, '2025-11-29 07:19:29', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (63, 17, '2025-11-29 07:20:01', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (64, 18, '2025-11-29 07:20:33', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (65, 2, '2025-11-29 18:42:25', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (66, 4, '2025-11-29 18:42:58', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (67, 5, '2025-11-29 18:43:30', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (68, 6, '2025-11-29 18:44:02', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (69, 7, '2025-11-29 18:44:34', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (70, 8, '2025-11-29 18:45:08', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (71, 9, '2025-11-29 18:45:41', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (72, 10, '2025-11-29 18:46:14', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (73, 11, '2025-11-29 18:46:46', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (74, 12, '2025-11-29 18:47:19', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (75, 13, '2025-11-29 18:47:52', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (76, 14, '2025-11-29 18:48:25', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (77, 15, '2025-11-29 18:48:58', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (78, 16, '2025-11-29 18:49:31', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (79, 17, '2025-11-29 18:50:04', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (80, 18, '2025-11-29 18:50:36', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (81, 2, '2025-11-30 06:12:24', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (82, 4, '2025-11-30 06:12:55', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (83, 5, '2025-11-30 06:13:29', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (84, 6, '2025-11-30 06:14:01', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (85, 7, '2025-11-30 06:14:33', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (86, 8, '2025-11-30 06:15:07', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (87, 9, '2025-11-30 06:15:40', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (88, 10, '2025-11-30 06:16:13', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (89, 11, '2025-11-30 06:16:45', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (90, 12, '2025-11-30 06:17:18', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (91, 13, '2025-11-30 06:17:50', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (92, 14, '2025-11-30 06:18:22', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (93, 15, '2025-11-30 06:18:55', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (94, 16, '2025-11-30 06:19:28', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (95, 17, '2025-11-30 06:20:01', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (96, 18, '2025-11-30 06:20:35', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (97, 2, '2025-11-30 17:42:24', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (98, 4, '2025-11-30 17:42:56', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (99, 5, '2025-11-30 17:43:29', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (100, 6, '2025-11-30 17:44:01', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (101, 7, '2025-11-30 17:44:34', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (102, 8, '2025-11-30 17:45:06', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (103, 9, '2025-11-30 17:45:39', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (104, 10, '2025-11-30 17:46:11', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (105, 11, '2025-11-30 17:46:44', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (106, 12, '2025-11-30 17:47:16', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (107, 13, '2025-11-30 17:47:48', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (108, 14, '2025-11-30 17:48:21', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (109, 15, '2025-11-30 17:48:53', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (110, 16, '2025-11-30 17:49:25', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (111, 17, '2025-11-30 17:49:57', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (112, 18, '2025-11-30 17:50:28', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (113, 2, '2025-12-01 05:12:24', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (114, 4, '2025-12-01 05:12:57', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (115, 5, '2025-12-01 05:13:31', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (116, 6, '2025-12-01 05:14:03', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (117, 7, '2025-12-01 05:14:36', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (118, 8, '2025-12-01 05:15:10', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (119, 9, '2025-12-01 05:15:42', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (120, 10, '2025-12-01 05:16:15', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (121, 11, '2025-12-01 05:16:47', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (122, 12, '2025-12-01 05:17:19', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (123, 13, '2025-12-01 05:17:52', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (124, 14, '2025-12-01 05:18:25', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (125, 15, '2025-12-01 05:18:58', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (126, 16, '2025-12-01 05:19:30', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (127, 17, '2025-12-01 05:20:03', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (128, 18, '2025-12-01 05:20:35', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (129, 9, '2025-12-01 14:40:09', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (130, 10, '2025-12-01 14:40:16', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (131, 11, '2025-12-01 14:40:23', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (132, 12, '2025-12-01 14:40:30', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (133, 13, '2025-12-01 14:40:38', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (134, 14, '2025-12-01 14:40:46', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (135, 15, '2025-12-01 14:40:53', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (136, 16, '2025-12-01 14:41:01', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (137, 17, '2025-12-01 14:41:09', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (138, 18, '2025-12-01 14:41:17', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (139, 8, '2025-12-01 17:40:09', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (140, 2, '2025-12-01 18:10:09', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (141, 4, '2025-12-01 18:10:17', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (142, 5, '2025-12-01 18:10:24', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (143, 6, '2025-12-01 18:10:31', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (144, 7, '2025-12-01 18:10:38', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (145, 9, '2025-12-02 00:10:09', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (146, 10, '2025-12-02 00:10:16', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (147, 11, '2025-12-02 00:10:24', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (148, 12, '2025-12-02 00:10:31', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (149, 13, '2025-12-02 00:10:38', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (150, 14, '2025-12-02 00:10:45', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (151, 15, '2025-12-02 00:10:53', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (152, 16, '2025-12-02 00:11:00', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (153, 17, '2025-12-02 00:11:08', 'success', NULL);
INSERT INTO `crawl_logs` VALUES (154, 18, '2025-12-02 00:11:16', 'success', NULL);

-- ----------------------------
-- Table structure for system_configs
-- ----------------------------
DROP TABLE IF EXISTS `system_configs`;
CREATE TABLE `system_configs`  (
  `key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`key`) USING BTREE,
  INDEX `ix_system_configs_key`(`key` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_configs
-- ----------------------------
INSERT INTO `system_configs` VALUES ('expired_days', '1', '提醒阈值(天)');
INSERT INTO `system_configs` VALUES ('webhook_daily_time', '10:00', '每日推送时间');
INSERT INTO `system_configs` VALUES ('webhook_url', 'https://oapi.dingtalk.com/robot/send?access_token=a754fa50a08002482e1a77a9567fdcb88c0d15aecf310f6ec1a9605bfc3b43ca', 'Webhook URL');
INSERT INTO `system_configs` VALUES ('weibo_cookie', 'SCF=AiFSa_8afZr7oy9o0B1h8EJk69HMvVwIFRzvPLrZq9QKkH6xxUBHJamY6u8-cb0QYlAl3ClUrdYU91_AWpdv0F4.; SUB=_2A25EIsSKDeRhGeFL6FMZ8CvEzD6IHXVnXlhCrDV8PUNbmtAbLXn7kW9NQicp6JtBf4nCJf95p8UaMWkkrxvQJ955; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWL8CfTX64m6GCuUEYBaEAf5JpX5KzhUgL.FoMfe02Reh-RS0z2dJLoIEBLxKqL1KnL12-LxKnLBKeL1K-LxK-LB-BLBKqLxK.L1K-LB.qt; ALF=02_1766736346; SINAGLOBAL=6214856956496.17.1764144349848; XSRF-TOKEN=ypgUZXZYHwz_YzxtGJWHp1mT; _s_tentry=weibo.com; Apache=564121629464.9576.1764204797307; ULV=1764204797314:2:2:2:564121629464.9576.1764204797307:1764144349851; WBPSESS=NCOoEdes9Q-ovLA96k552MkuOxz6uokd_jOFz2PUI1ZdWcBLPeOkJTlKvsqjI1XZgI0wMQ4TytXgakmcfEvgegekIJ1cebPza1mwtNbuTtPwN5cuwW-CIAWGisw5RrxFQ0h2WmNgXv3vVAo_Q6hRzQ==', 'Weibo Crawler Cookie');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `hashed_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `is_active` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_users_username`(`username` ASC) USING BTREE,
  INDEX `ix_users_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'boyueadmin', '$2b$12$7JywIPtLP/h4K18ZtTsJXeb6/j4F95iVg/jBzU8BNvOYhF.gSNKS2', 1);
INSERT INTO `users` VALUES (2, 'admin', '$2b$12$Dsxa63dax16VGuizJGIjU.xc32NxA1jzkALsd8LDtH/ogDbhKcDCO', 1);

-- ----------------------------
-- Table structure for weibo_accounts
-- ----------------------------
DROP TABLE IF EXISTS `weibo_accounts`;
CREATE TABLE `weibo_accounts`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `screen_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `last_update_time` datetime NULL DEFAULT NULL,
  `last_check_time` datetime NULL DEFAULT NULL,
  `status` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `check_interval` int NULL DEFAULT NULL,
  `is_active` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_weibo_accounts_uid`(`uid` ASC) USING BTREE,
  INDEX `ix_weibo_accounts_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of weibo_accounts
-- ----------------------------
INSERT INTO `weibo_accounts` VALUES (2, '2560987592', '淮安警方', '2025-12-01 17:02:28', '2025-12-02 02:10:09', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (4, '1988114471', '乐行淮安', '2025-12-01 17:10:51', '2025-12-02 02:10:17', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (5, '5165082681', '淮安网警', '2025-12-01 17:28:39', '2025-12-02 02:10:24', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (6, '3463895610', '淮安司法行政', '2025-11-27 11:38:36', '2025-12-02 02:10:31', 'expired', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (7, '3082306563', '淮安生态环境', '2025-11-28 15:52:35', '2025-12-02 02:10:38', 'expired', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (8, '2593303232', '淮安市交通运输局', '2025-12-01 16:13:43', '2025-12-02 01:40:09', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (9, '3572501595', '淮安经开区', '2025-12-01 14:36:26', '2025-12-02 08:10:09', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (10, '1900943327', '盱眙发布', '2025-12-01 08:43:07', '2025-12-02 08:10:16', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (11, '3585297153', '涟水发布', '2025-12-01 14:59:06', '2025-12-02 08:10:24', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (12, '3610251403', '爱心淮阴', '2025-11-28 16:06:16', '2025-12-02 08:10:31', 'expired', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (13, '3581770931', '清江浦发布', '2025-12-01 16:48:10', '2025-12-02 08:10:38', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (14, '2607861430', '淮阴警方', '2025-12-01 16:32:35', '2025-12-02 08:10:45', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (15, '7801678707', '水韵金湖', '2025-12-01 21:13:16', '2025-12-02 08:10:53', 'normal', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (16, '7805745062', '淮安区政务', '2025-11-28 18:40:02', '2025-12-02 08:11:00', 'expired', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (17, '7772775695', '淮安区警方', '2025-11-28 16:06:06', '2025-12-02 08:11:08', 'expired', 3600, 1);
INSERT INTO `weibo_accounts` VALUES (18, '7959600592', '洪泽政务', '2025-11-30 11:05:21', '2025-12-02 08:11:16', 'expired', 3600, 1);

SET FOREIGN_KEY_CHECKS = 1;
