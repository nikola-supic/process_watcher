-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 29, 2021 at 11:25 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `process_watcher`
--

-- --------------------------------------------------------

--
-- Table structure for table `apps`
--

CREATE TABLE `apps` (
  `id` int(11) NOT NULL,
  `name` varchar(24) NOT NULL,
  `caption` varchar(24) NOT NULL,
  `type` varchar(24) NOT NULL,
  `date` datetime NOT NULL,
  `daily` int(11) NOT NULL,
  `monthly` int(11) NOT NULL,
  `yearly` int(11) NOT NULL,
  `all_time` int(11) NOT NULL,
  `time_started` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `apps`
--

INSERT INTO `apps` (`id`, `name`, `caption`, `type`, `date`, `daily`, `monthly`, `yearly`, `all_time`, `time_started`) VALUES
(1, 'Steam', 'steam.exe', 'Gaming', '2021-03-21 10:59:46', 0, 0, 0, 0, '0000-00-00 00:00:00'),
(2, 'Sublime Text', 'sublime_text.exe', 'Learning', '2021-03-21 11:00:38', 0, 0, 2, 2, '0000-00-00 00:00:00'),
(3, 'MS Edge', 'msedge.exe', 'Browsing', '2021-06-29 11:17:53', 233, 233, 235, 235, '0000-00-00 00:00:00'),
(4, 'CMD', 'ConEmuC64.exe', 'Learning', '2021-06-29 11:17:53', 233, 233, 235, 235, '0000-00-00 00:00:00'),
(5, 'GitHub', 'GitHubDesktop.exe', 'Learning', '2021-06-29 11:17:53', 233, 233, 233, 233, '0000-00-00 00:00:00'),
(6, 'VLC', 'vlc.exe', 'Learning', '2021-03-21 11:00:07', 0, 0, 0, 0, '0000-00-00 00:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `apps`
--
ALTER TABLE `apps`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `apps`
--
ALTER TABLE `apps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
