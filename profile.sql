-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 07, 2025 at 10:55 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `profile`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `sno` int(11) NOT NULL,
  `name` text NOT NULL,
  `phone_num` varchar(12) NOT NULL,
  `msg` varchar(120) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `email` varchar(50) NOT NULL,
  `umail` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`sno`, `name`, `phone_num`, `msg`, `date`, `email`, `umail`) VALUES
(1, 'JIGNESH SATHAVARA', '7016429311', 'hi', '2025-04-07 13:56:07', 'hsgoswami18@gmail.com', 'sathvarajigar2@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `edcs`
--

CREATE TABLE `edcs` (
  `sno` int(11) NOT NULL,
  `cor_duration` varchar(20) NOT NULL,
  `clg_name` varchar(50) NOT NULL,
  `clg_add` varchar(50) NOT NULL,
  `cor_name` varchar(25) NOT NULL,
  `cor_work` varchar(50) NOT NULL,
  `content` varchar(120) NOT NULL,
  `post_date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `edcs`
--

INSERT INTO `edcs` (`sno`, `cor_duration`, `clg_name`, `clg_add`, `cor_name`, `cor_work`, `content`, `post_date`) VALUES
(1, '2022-2025', 'Shri sarvjanik BCA & PGDCA college', 'Mahesana,Gujarat,India', 'BCA', 'Web Devlopment', 'I am bca student in shri sarvjanik bca & pgdca college and lern about C, HTML, PHP, .NET, PYTHON, JAVA.', '2024-11-23 14:54:02');

-- --------------------------------------------------------

--
-- Table structure for table `expes`
--

CREATE TABLE `expes` (
  `sno` int(11) NOT NULL,
  `join_date` varchar(12) NOT NULL,
  `title` varchar(30) NOT NULL,
  `company_name` varchar(50) NOT NULL,
  `content` varchar(240) NOT NULL,
  `com_add` varchar(30) NOT NULL,
  `res_date` varchar(12) NOT NULL,
  `post_date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `expes`
--

INSERT INTO `expes` (`sno`, `join_date`, `title`, `company_name`, `content`, `com_add`, `res_date`, `post_date`) VALUES
(1, 'AUG-2022', 'Software service provider', 'SIDDHI COMPUTERS', 'In this company Manage large amounts of inbound and outbound calls in a timely manner.Identify customers’ needs, clarify information, research every issue and provide solutions and/or alternatives..', 'Mahesana,Gujarat,India', 'APR-2024', '2024-11-23 14:56:58');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `sno` int(11) NOT NULL,
  `title` varchar(80) NOT NULL,
  `pro_link` varchar(300) NOT NULL,
  `content` varchar(200) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `img_file` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`sno`, `title`, `pro_link`, `content`, `date`, `img_file`) VALUES
(1, 'Project 1', 'thejignesh.in', 'Hey! This is my portfolio website it\'s create by using html,css,python.', '2024-11-28 11:09:52', 'project1.png');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `uname` varchar(30) NOT NULL,
  `umail` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `reset_token` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `uname`, `umail`, `password`, `reset_token`) VALUES
(2, 'JIGNESH SATHAVARA', 'sathvarajigar2@gmail.com', 'Jigar@123', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `edcs`
--
ALTER TABLE `edcs`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `expes`
--
ALTER TABLE `expes`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `edcs`
--
ALTER TABLE `edcs`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `expes`
--
ALTER TABLE `expes`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
