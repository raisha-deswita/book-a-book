/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_library_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_library_user_id` FOREIGN KEY (`user_id`) REFERENCES `library_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_activitylog`;
CREATE TABLE `library_activitylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(255) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `library_activitylog_user_id_86830a20_fk_library_user_id` (`user_id`),
  CONSTRAINT `library_activitylog_user_id_86830a20_fk_library_user_id` FOREIGN KEY (`user_id`) REFERENCES `library_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_book`;
CREATE TABLE `library_book` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `isbn` varchar(20) NOT NULL,
  `publisher` varchar(255) NOT NULL,
  `publication_year` int NOT NULL,
  `publication_place` varchar(255) DEFAULT NULL,
  `page_count` int NOT NULL,
  `edition` varchar(50) DEFAULT NULL,
  `dimensions` varchar(50) DEFAULT NULL,
  `cover_material` varchar(50) DEFAULT NULL,
  `cover_image` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  `synopsis` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `isbn` (`isbn`),
  KEY `library_book_category_id_c90a2d6d_fk_library_category_id` (`category_id`),
  CONSTRAINT `library_book_category_id_c90a2d6d_fk_library_category_id` FOREIGN KEY (`category_id`) REFERENCES `library_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_bookitem`;
CREATE TABLE `library_bookitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `book_code` varchar(50) NOT NULL,
  `condition` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `location` varchar(100) DEFAULT NULL,
  `book_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `book_code` (`book_code`),
  KEY `library_bookitem_book_id_8c347850_fk_library_book_id` (`book_id`),
  CONSTRAINT `library_bookitem_book_id_8c347850_fk_library_book_id` FOREIGN KEY (`book_id`) REFERENCES `library_book` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_borrowing`;
CREATE TABLE `library_borrowing` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `borrow_date` datetime(6) NOT NULL,
  `due_date` datetime(6) NOT NULL,
  `fine_snapshot` int unsigned NOT NULL,
  `status` varchar(20) NOT NULL,
  `remarks` longtext,
  `approved_by_id` bigint DEFAULT NULL,
  `book_item_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `library_borrowing_approved_by_id_2540a90d_fk_library_user_id` (`approved_by_id`),
  KEY `library_borrowing_book_item_id_747b9b9b_fk_library_bookitem_id` (`book_item_id`),
  KEY `library_borrowing_user_id_b9b4ca75_fk_library_user_id` (`user_id`),
  CONSTRAINT `library_borrowing_approved_by_id_2540a90d_fk_library_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `library_user` (`id`),
  CONSTRAINT `library_borrowing_book_item_id_747b9b9b_fk_library_bookitem_id` FOREIGN KEY (`book_item_id`) REFERENCES `library_bookitem` (`id`),
  CONSTRAINT `library_borrowing_user_id_b9b4ca75_fk_library_user_id` FOREIGN KEY (`user_id`) REFERENCES `library_user` (`id`),
  CONSTRAINT `library_borrowing_chk_1` CHECK ((`fine_snapshot` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_category`;
CREATE TABLE `library_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `fine_per_day` int unsigned NOT NULL,
  `loan_duration_days` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `library_category_chk_1` CHECK ((`fine_per_day` >= 0)),
  CONSTRAINT `library_category_chk_2` CHECK ((`loan_duration_days` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_librarianprofile`;
CREATE TABLE `library_librarianprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(50) NOT NULL,
  `position` varchar(100) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `library_librarianprofile_user_id_3aecd76c_fk_library_user_id` FOREIGN KEY (`user_id`) REFERENCES `library_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_returnrecord`;
CREATE TABLE `library_returnrecord` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `return_date` datetime(6) NOT NULL,
  `late_days` int unsigned NOT NULL,
  `total_fine` int unsigned NOT NULL,
  `fine_status` varchar(20) NOT NULL,
  `return_condition` varchar(20) NOT NULL,
  `borrowing_id` bigint NOT NULL,
  `received_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `borrowing_id` (`borrowing_id`),
  KEY `library_returnrecord_received_by_id_c1e85c72_fk_library_user_id` (`received_by_id`),
  CONSTRAINT `library_returnrecord_borrowing_id_3c012c62_fk_library_b` FOREIGN KEY (`borrowing_id`) REFERENCES `library_borrowing` (`id`),
  CONSTRAINT `library_returnrecord_received_by_id_c1e85c72_fk_library_user_id` FOREIGN KEY (`received_by_id`) REFERENCES `library_user` (`id`),
  CONSTRAINT `library_returnrecord_chk_1` CHECK ((`late_days` >= 0)),
  CONSTRAINT `library_returnrecord_chk_2` CHECK ((`total_fine` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_studentprofile`;
CREATE TABLE `library_studentprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nisn` varchar(20) NOT NULL,
  `class_name` varchar(50) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nisn` (`nisn`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `library_studentprofile_user_id_71250400_fk_library_user_id` FOREIGN KEY (`user_id`) REFERENCES `library_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_user`;
CREATE TABLE `library_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `address` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_user_groups`;
CREATE TABLE `library_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `library_user_groups_user_id_group_id_89ea2476_uniq` (`user_id`,`group_id`),
  KEY `library_user_groups_group_id_a225a4a9_fk_auth_group_id` (`group_id`),
  CONSTRAINT `library_user_groups_group_id_a225a4a9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `library_user_groups_user_id_797ccc7b_fk_library_user_id` FOREIGN KEY (`user_id`) REFERENCES `library_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `library_user_user_permissions`;
CREATE TABLE `library_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `library_user_user_permis_user_id_permission_id_aed1df16_uniq` (`user_id`,`permission_id`),
  KEY `library_user_user_pe_permission_id_6a5167f4_fk_auth_perm` (`permission_id`),
  CONSTRAINT `library_user_user_pe_permission_id_6a5167f4_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `library_user_user_pe_user_id_d9d78974_fk_library_u` FOREIGN KEY (`user_id`) REFERENCES `library_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add book', 7, 'add_book'),
(22, 'Can change book', 7, 'change_book'),
(23, 'Can delete book', 7, 'delete_book'),
(24, 'Can view book', 7, 'view_book'),
(25, 'Can add Category', 10, 'add_category'),
(26, 'Can change Category', 10, 'change_category'),
(27, 'Can delete Category', 10, 'delete_category'),
(28, 'Can view Category', 10, 'view_category'),
(29, 'Can add User Account', 14, 'add_user'),
(30, 'Can change User Account', 14, 'change_user'),
(31, 'Can delete User Account', 14, 'delete_user'),
(32, 'Can view User Account', 14, 'view_user'),
(33, 'Can add Activity Log', 6, 'add_activitylog'),
(34, 'Can change Activity Log', 6, 'change_activitylog'),
(35, 'Can delete Activity Log', 6, 'delete_activitylog'),
(36, 'Can view Activity Log', 6, 'view_activitylog'),
(37, 'Can add Physical Book Item', 8, 'add_bookitem'),
(38, 'Can change Physical Book Item', 8, 'change_bookitem'),
(39, 'Can delete Physical Book Item', 8, 'delete_bookitem'),
(40, 'Can view Physical Book Item', 8, 'view_bookitem'),
(41, 'Can add borrowing', 9, 'add_borrowing'),
(42, 'Can change borrowing', 9, 'change_borrowing'),
(43, 'Can delete borrowing', 9, 'delete_borrowing'),
(44, 'Can view borrowing', 9, 'view_borrowing'),
(45, 'Can add librarian profile', 11, 'add_librarianprofile'),
(46, 'Can change librarian profile', 11, 'change_librarianprofile'),
(47, 'Can delete librarian profile', 11, 'delete_librarianprofile'),
(48, 'Can view librarian profile', 11, 'view_librarianprofile'),
(49, 'Can add return record', 12, 'add_returnrecord'),
(50, 'Can change return record', 12, 'change_returnrecord'),
(51, 'Can delete return record', 12, 'delete_returnrecord'),
(52, 'Can view return record', 12, 'view_returnrecord'),
(53, 'Can add student profile', 13, 'add_studentprofile'),
(54, 'Can change student profile', 13, 'change_studentprofile'),
(55, 'Can delete student profile', 13, 'delete_studentprofile'),
(56, 'Can view student profile', 13, 'view_studentprofile');
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2026-04-22 12:51:31.114862', '1', 'American Literature', 1, '[{\"added\": {}}]', 10, 1),
(2, '2026-04-22 12:51:36.584402', '1', 'Red, White and Royal Blue', 1, '[{\"added\": {}}]', 7, 1),
(3, '2026-04-22 12:51:51.122249', '1', 'Red, White and Royal Blue', 2, '[{\"changed\": {\"fields\": [\"Cover image\"]}}]', 7, 1),
(4, '2026-04-22 13:03:41.562793', '2', 'Game Changer', 1, '[{\"added\": {}}]', 7, 1),
(5, '2026-04-22 13:05:27.205697', '3', 'Heated Rivalry', 1, '[{\"added\": {}}]', 7, 1),
(6, '2026-04-22 13:09:00.597289', '2', 'Korean Fiction', 1, '[{\"added\": {}}]', 10, 1),
(7, '2026-04-22 13:16:43.201850', '4', 'Omniscient Reader\'s Viewpoint (Novel)', 1, '[{\"added\": {}}]', 7, 1),
(8, '2026-04-22 13:18:43.578336', '5', 'Omniscient Reader\'s Viewpoint', 1, '[{\"added\": {}}]', 7, 1),
(9, '2026-04-22 13:19:08.428493', '5', 'Omniscient Reader\'s Viewpoint (Novel)', 2, '[{\"changed\": {\"fields\": [\"Title\"]}}]', 7, 1),
(10, '2026-04-22 13:31:10.149570', '6', 'The Long Game', 1, '[{\"added\": {}}]', 7, 1),
(11, '2026-04-23 01:13:37.340336', '3', 'librarian123', 1, '[{\"added\": {}}]', 14, 1),
(12, '2026-04-23 01:14:53.589003', '3', 'librarian123', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\"]}}]', 14, 1),
(13, '2026-04-23 04:02:23.900155', '1', 'RWRB2024 - Red, White and Royal Blue', 1, '[{\"added\": {}}]', 8, 1),
(14, '2026-04-23 05:23:21.249050', '1', 'RWRB2024-01 - Red, White and Royal Blue', 2, '[{\"changed\": {\"fields\": [\"Book code\"]}}]', 8, 1),
(15, '2026-04-23 05:23:45.512778', '2', 'RWRB2024-02 - Red, White and Royal Blue', 1, '[{\"added\": {}}]', 8, 1),
(16, '2026-04-23 05:24:08.864133', '3', 'GC2025-01 - Game Changer', 1, '[{\"added\": {}}]', 8, 1),
(17, '2026-04-23 05:24:28.754460', '4', 'HR2024-01 - Heated Rivalry', 1, '[{\"added\": {}}]', 8, 1),
(18, '2026-04-23 05:24:55.662525', '5', 'ORV2026-V101 - Omniscient Reader\'s Viewpoint (Novel)', 1, '[{\"added\": {}}]', 8, 1),
(19, '2026-04-23 05:25:54.362849', '6', 'ORV2026-V201 - Omniscient Reader\'s Viewpoint (Novel)', 1, '[{\"added\": {}}]', 8, 1),
(20, '2026-04-23 05:26:10.351264', '7', 'TLG - The Long Game', 1, '[{\"added\": {}}]', 8, 1),
(21, '2026-04-23 05:26:29.144679', '7', 'TLG2026-01 - The Long Game', 2, '[{\"changed\": {\"fields\": [\"Book code\"]}}]', 8, 1),
(22, '2026-04-23 08:28:46.330926', '4', 'rach_mcreid borrowed HR2024-01', 2, '[{\"changed\": {\"fields\": [\"Due date\"]}}]', 9, 1),
(23, '2026-04-24 00:07:28.127865', '7', 'ilyarozanov borrowed TLG2026-01', 2, '[{\"changed\": {\"fields\": [\"Due date\"]}}]', 9, 1),
(24, '2026-04-24 00:13:43.360102', '8', 'ilyarozanov borrowed TLG2026-01', 2, '[{\"changed\": {\"fields\": [\"Due date\"]}}]', 9, 1),
(25, '2026-04-24 00:15:17.439881', '9', 'ilyarozanov borrowed RWRB2024-01', 2, '[{\"changed\": {\"fields\": [\"Borrow date\", \"Due date\"]}}]', 9, 1);
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'library', 'activitylog'),
(7, 'library', 'book'),
(8, 'library', 'bookitem'),
(9, 'library', 'borrowing'),
(10, 'library', 'category'),
(11, 'library', 'librarianprofile'),
(12, 'library', 'returnrecord'),
(13, 'library', 'studentprofile'),
(14, 'library', 'user');
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-04-22 09:02:54.324557'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-04-22 09:02:54.382704'),
(3, 'auth', '0001_initial', '2026-04-22 09:02:54.602925'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-04-22 09:02:54.657711'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-04-22 09:02:54.662861'),
(6, 'auth', '0004_alter_user_username_opts', '2026-04-22 09:02:54.667817'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-04-22 09:02:54.673130'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-04-22 09:02:54.676458'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-04-22 09:02:54.681057'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-04-22 09:02:54.685136'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-04-22 09:02:54.689420'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-04-22 09:02:54.740402'),
(13, 'auth', '0011_update_proxy_permissions', '2026-04-22 09:02:54.746177'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-04-22 09:02:54.750574'),
(15, 'library', '0001_initial', '2026-04-22 09:02:55.852260'),
(16, 'admin', '0001_initial', '2026-04-22 09:02:55.978035'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-04-22 09:02:55.990371'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-04-22 09:02:55.998515'),
(19, 'sessions', '0001_initial', '2026-04-22 09:02:56.040283'),
(20, 'library', '0002_book_synopsis', '2026-04-23 01:01:43.400084'),
(21, 'library', '0003_category_loan_duration_days_and_more', '2026-04-23 07:17:13.937347');
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('i1l6pwfncymscuz1z98y1ja2m10m960n', '.eJxVjLEKwjAUAP_lzVKS1CRNR8FRnJzLe8kLDca2JO0g4r-L0EHXO-5eMOC2jsNWuQwpQA8SDr-M0N95-gpclpw8rmmeapMTFSzPZte1OT8w5Wu5VS4TPvgyB86nvf0bjlhH6MEqo4m0tF2rOmEUKkc2cGvIi2iicxg0G4mCpUTjhWWU2sbYakdHHy28Pz5NPnU:1wG7vo:_xZjAMf6es3U2ph48mtx4oGsD0iPJJlp9Tnl2PFjtpQ', '2026-05-08 04:14:20.913208'),
('w7pi3brl4lj2an0f0cxodnkfmcn9yzng', '.eJxVjD0LwjAUAP9LZilJk6ZJR8FRnJzLe3mvNJh-kLSDiP9dhA663nH3Ej3s29jvhXMfSXTCitMvQwgPnr8C1jXFAFtc5lKliBnyszp0qS4TxHTL98J5homvC3E6H-3fcIQyik60apBKS8_KSytJtcFY0MrQ4ILT0qI2SLX2jp1BRwZqi8QWG1QNeAji_QEwVT46:1wG5EU:VVK3zQ-kaK95Pi7SHg02Gn1UuUZZi45Ykoyd2KnzKYA', '2026-05-08 01:21:26.617451');

INSERT INTO `library_book` (`id`, `title`, `author`, `isbn`, `publisher`, `publication_year`, `publication_place`, `page_count`, `edition`, `dimensions`, `cover_material`, `cover_image`, `created_at`, `category_id`, `synopsis`) VALUES
(1, 'Red, White and Royal Blue', 'Casey McQuiston', '978-1035028504', 'Pan Macmillan', 2023, 'London', 384, 'Movie Tie-In Edition (2023)', '5.12 x 0.94 x 7.76 inches', 'Paperback', 'book_covers/-RED_WHITE__ROYAL_BLUE-.jpg', '2026-04-22 12:51:36.583803', 1, NULL),
(2, 'Game Changer', 'Rachelle Goguen', '978-1335534620', 'Carina Press', 2026, 'Toronto', 368, 'Media Tie-Ins Edition', '5.30 x 7.90 x 1.10 inches', 'Paperback', 'book_covers/Game_Changer__Rachel_Reid__9781335534620.jpg', '2026-04-22 13:03:41.561230', 1, NULL),
(3, 'Heated Rivalry', 'Rachelle Goguen', '978-1335534637', 'Carina Press', 2024, 'Toronto', 416, 'Media Tie-Ins Edition', '5.24 x 7.97 x 1.00 inches', 'Paperback', 'book_covers/Heated_Rivalry__Now_Streaming_on_Crave_and_HBO_Max_Game_Changers_2.jpg', '2026-04-22 13:05:27.203578', 1, NULL),
(4, 'Omniscient Reader\'s Viewpoint (Novel)', 'singNsong', '979-8400903526', 'Ize Press', 2025, 'New York', 260, 'Vol 1', '5.75 x 0.65 x 8.3 Inches', 'Die-cut cover, Cardstock', 'book_covers/download_10.jpg', '2026-04-22 13:16:43.199515', 2, NULL),
(5, 'Omniscient Reader\'s Viewpoint (Novel)', 'singNsong', '979-8400903762', 'Ize Press', 2026, 'New York', 268, 'Vol 3', '5.80 x 0.67 x 8.3 Inches', 'Die-cut cover, Cardstock', 'book_covers/Omniscient_Readers_Viewpoint.jpg', '2026-04-22 13:18:43.577051', 2, NULL),
(6, 'The Long Game', 'Rachelle Goguen', '978-1335534644', 'Carina Press', 2022, 'Toronto', 416, 'Media Tie-Ins Edition', '5.26 x 7.95 x 0.98', 'Paperback', 'book_covers/The_Long_Game_IJZJbN5.jpg', '2026-04-22 13:31:10.146743', 1, 'None'),
(8, 'Harry Potter', 'J.K Rowling', '978-82930111', 'Gramedia', 2012, 'London', 127, 'Vol 4', '12 x 21', 'Paperback', 'book_covers/download_10_jlfitw3.jpg', '2026-04-23 06:40:57.301158', 1, 'ini sinopsis');
INSERT INTO `library_bookitem` (`id`, `book_code`, `condition`, `status`, `location`, `book_id`) VALUES
(1, 'RWRB2024-01', 'good', 'available', 'Shelf-02', 1),
(2, 'RWRB2024-02', 'slightly_damaged', 'available', 'Shelf-02', 1),
(3, 'GC2025-01', 'good', 'available', 'Shelf-02', 2),
(4, 'HR2024-01', 'good', 'available', 'Shelf-02', 3),
(5, 'ORV2026-V101', 'good', 'available', NULL, 4),
(6, 'ORV2026-V201', 'good', 'available', 'Shelf-03', 5),
(7, 'TLG2026-01', 'good', 'borrowed', 'Shelf-04', 6);
INSERT INTO `library_borrowing` (`id`, `borrow_date`, `due_date`, `fine_snapshot`, `status`, `remarks`, `approved_by_id`, `book_item_id`, `user_id`) VALUES
(1, '2026-04-23 04:03:21.706854', '2026-04-30 04:03:21.706747', 5000, 'returned', NULL, 3, 1, 2),
(2, '2026-04-23 04:57:26.886616', '2026-04-30 04:57:26.886499', 5000, 'returned', NULL, 3, 1, 2),
(3, '2026-04-23 05:33:10.663288', '2026-04-30 05:33:10.663176', 5000, 'returned', NULL, 1, 3, 2),
(4, '2026-04-23 07:04:58.000000', '2026-04-23 08:28:41.000000', 5000, 'returned', '', 1, 4, 2),
(5, '2026-04-23 07:07:52.885001', '2026-04-30 07:07:52.884858', 5000, 'returned', NULL, 1, 7, 2),
(7, '2026-04-23 23:47:15.000000', '2026-04-24 00:07:26.000000', 5000, 'returned', '', 1, 7, 4),
(8, '2026-04-24 00:13:10.000000', '2026-04-25 00:13:36.000000', 5000, 'returned', '', 1, 7, 4),
(9, '2026-04-23 23:00:00.000000', '2026-04-24 23:15:00.000000', 5000, 'returned', '', 1, 1, 4),
(10, '2026-04-24 01:02:24.130598', '2026-05-01 01:02:24.130598', 5000, 'returned', NULL, 1, 6, 4),
(11, '2026-04-24 01:22:53.277276', '2026-05-01 01:22:53.277276', 5000, 'returned', NULL, 1, 1, 6),
(12, '2026-04-24 02:24:56.536240', '2026-05-01 02:24:56.536240', 5000, 'returned', NULL, 1, 3, 6),
(13, '2026-04-24 04:26:59.099464', '2026-04-24 23:59:59.099464', 5000, 'active', NULL, 1, 7, 6);
INSERT INTO `library_category` (`id`, `name`, `description`, `fine_per_day`, `loan_duration_days`) VALUES
(1, 'American Literature', 'American Literature', 5000, 7),
(2, 'Korean Fiction', 'Koren Fiction books', 5000, 7),
(3, 'Fiction Literature', NULL, 1000, 3);

INSERT INTO `library_returnrecord` (`id`, `return_date`, `late_days`, `total_fine`, `fine_status`, `return_condition`, `borrowing_id`, `received_by_id`) VALUES
(1, '2026-04-23 04:56:02.469288', 0, 0, 'not_applicable', 'good', 1, 3),
(2, '2026-04-23 05:01:11.671936', 0, 0, 'not_applicable', 'good', 2, 3),
(3, '2026-04-23 05:33:30.516475', 0, 0, 'not_applicable', 'damaged', 3, 1),
(4, '2026-04-23 08:29:24.179148', 1, 5000, 'paid', 'good', 4, 1),
(5, '2026-04-23 08:29:42.311383', 0, 0, 'not_applicable', 'good', 5, 1),
(6, '2026-04-24 00:07:49.608914', 1, 5000, 'paid', 'good', 7, 1),
(7, '2026-04-24 00:13:54.797083', 0, 0, 'not_applicable', 'good', 8, 1),
(8, '2026-04-24 00:15:38.621403', 0, 0, 'not_applicable', 'good', 9, 1),
(9, '2026-04-24 01:23:47.450678', 0, 0, 'not_applicable', 'good', 11, 1),
(10, '2026-04-24 03:11:17.590431', 0, 0, 'not_applicable', 'good', 10, 1),
(11, '2026-04-24 03:11:28.070529', 0, 0, 'not_applicable', 'good', 12, 1);

INSERT INTO `library_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `phone_number`, `address`) VALUES
(1, 'pbkdf2_sha256$1200000$hjWLhTVaaK5sXIsh6P8HZw$KgwT2PR7O90fIyymC/1TH2lSt6iCLCymDFC2VgSjsg0=', '2026-04-24 04:14:20.907148', 1, 'site-admin', '', '', '', 1, 1, '2026-04-22 12:19:22.272030', 'admin', 'None', 'None'),
(2, 'pbkdf2_sha256$1200000$o502hDb1R8DdbGQc2aomrd$rqSFPIGSYuo1MHpwz2BEULCEd81/Gm2u9q6UGMs07uY=', '2026-04-23 07:04:46.375732', 0, 'rach_mcreid', '', '', 'rachelmcquiston444@gmail.com', 0, 1, '2026-04-23 00:36:15.260647', 'student', NULL, NULL),
(3, 'pbkdf2_sha256$1200000$5UJvtNQ5hEweup3inCvkbf$FaKABWnDqbJEDmNqlnq+pX1ofJpYak03crJXuha2x2g=', '2026-04-23 04:59:44.953167', 0, 'librarian123', 'Rini', 'Ridansyah', 'rini@gmail.com', 1, 1, '2026-04-23 01:13:36.000000', 'librarian', 'None', 'None'),
(4, 'pbkdf2_sha256$1200000$dife4JatI84E3qsOol4M1f$lG8GAXiJhZVoATHuf0rDpXc30hPuc4yE5e8eT2pnaOk=', '2026-04-23 21:14:24.592815', 0, 'ilyarozanov', '', '', 'ilyarozanov2121@gmail.com', 0, 1, '2026-04-23 20:15:38.919225', 'student', NULL, NULL),
(5, 'pbkdf2_sha256$1200000$0wOTLrZhDLxUY0hXNJngnQ$ejU8NJ1WRDNxJAGyJy6AU6oSvpfV/fBVfv6HaUjKXDg=', NULL, 1, 'site-admin2', 'Superuser', 'Hk', 'testing@gmail.com', 1, 1, '2026-04-24 00:05:20.523815', 'admin', '09289103221', 'Oak Street'),
(6, 'pbkdf2_sha256$1200000$R8p9Ruxd0HXEkeZ6KoiOUR$D3BnMVCyp0SZUsktTcnr/j8ATy/LObmBLvK2IwSpfGw=', '2026-04-24 01:21:26.610791', 0, 'usertesting1', '', '', 'usertesting@gmail.com', 0, 1, '2026-04-24 01:21:12.996103', 'student', NULL, NULL);




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;