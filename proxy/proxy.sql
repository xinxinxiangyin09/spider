/*
 Navicat MySQL Data Transfer

 Source Server         : pythonserver
 Source Server Type    : MySQL
 Source Server Version : 50727
 Source Host           : xxxxxxxxxxxxxxxxx
 Source Schema         : spider

 Target Server Type    : MySQL
 Target Server Version : 50727
 File Encoding         : 65001

 Date: 06/09/2019 18:52:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for proxy
-- ----------------------------
DROP TABLE IF EXISTS `proxy`;
CREATE TABLE `proxy`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '序列号',
  `content` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '代理IP，可直接使用',
  `now_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '爬取日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1251 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
