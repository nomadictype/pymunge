#!/usr/bin/perl

# Change the owner/group of all files in the specified tgz file to root/root.

use strict;
use Archive::Tar;

my $tar = Archive::Tar->new;
$tar->read($ARGV[0]);

my $filename;
for $filename ($tar->list_files()) {
	$tar->chown($filename, "root", "root");
}

$tar->write($ARGV[0], COMPRESS_GZIP);

