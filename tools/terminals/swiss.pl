#!/usr/bin/perl

# For use when perl is the only thing available
# Don't expect command line error checking

# For UDP, 'scan' doesn't really do much, we have to send some traffic to get a response

# Usage:  ./swiss.pl [-s/scan] [IP] [udp/tcp] [ports]
#         ./swiss.pl [-c/connect] [IP] [udp/tcp] [ports] < input
#		  ./swiss.pl [-r/resolve] [HOST/IP] [SERVER IP]
#
#  [ports] can be like 21-25,80,8888,443


# TODO: build a "resolve/-r flag"
# TODO: Parse DNS response
# TODO: support reverse lookup
# TODO: Add TXT record support

use IO::Socket;

sub scan{
	($ip,$port,$proto) = @_;
	my $sock = new IO::Socket::INET ( PeerAddr => $ip, PeerPort => $port, Proto => $proto, Timeout => 1);
#	die "Could not create socket: $!\n" unless $sock;
	if($sock){
		print("open ");
	}else{
		print("closed ");
	}
	print("$port/$proto\n");
	close($sock);
}

sub getports{
	local @ports;
	foreach $port (split(',',@_[0])){
		if($port =~ /(\d+)\-(\d+)/){
			for($i=$1;$i<=$2;$i++){
				push(@ports,$i);
			}
		}else{
			push(@ports,$port);
		}
	}
	return @ports;
}

sub go{
	($ip,$port,$proto) = @_;
	my $sock = new IO::Socket::INET ( PeerAddr => $ip, PeerPort => $port, Proto => $proto, Timeout => 2);
	die "Could not create socket: $!\n" unless $sock;

#	empty lines in an input file aren't the same as \r\n needed by HTTP
#	$test = "GET / HTTP/1.0\r\n\r\n";

	@data = <STDIN>;
	$blaa = "";
	foreach $line (@data){
		$line =~ s/\n/\r\n/g;
		$blaa .= $line;
	}
	print $sock $blaa;
	print while <$sock>; 
}

if($ARGV[0] eq "scan" || $ARGV[0] eq "-s"){
	@ports = getports($ARGV[3]);
	foreach $port (@ports){
		scan($ARGV[1],$port,$ARGV[2]);
	}
}elsif(($ARGV[0] eq "connect" || $ARGV[0] eq "-c")){
	@ports = getports($ARGV[3]);
	foreach $port (@ports){
		go($ARGV[1],$port,$ARGV[2]);
	}
}elsif(($ARGV[0] eq "resolve" || $ARGV[0] eq "-r")){
	# not using getaddr on purpose so we can override the DNS server setting

	my $sock = new IO::Socket::INET ( PeerAddr => $ARGV[2], PeerPort => '53', Proto => 'udp');
	die "Could not create socket: $!\n" unless $sock;
	$query = pack('H*','815001200001000000000000');

	# The query itself is a series of bytes and 'labels'
	# Each byte indicates how many characters are in the following label
	if($ARGV[1] =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)/){
		@labels = ($4,$3,$2,$1,'in-addr','arpa');
		$type = 'PTR';
	}else{
		$domain = $ARGV[1];
		@labels = split('\.',$domain);
		$type = 'A';
	}

# there's no pack/unpack for an 8bit integer, so we need to cheat
foreach $label (@labels){
	$bin8bit = substr(unpack('B*',pack('i*',length($label))),0,8);
	$query .= pack('B*',$bin8bit);
#	$bin8bit = substr(unpack('B*',pack('i*',length($label))),0,8);
	$query .= pack('a*',$label);
}


if($type eq 'A'){
	$query .= pack('H*','0000010001'); 
}elsif($type eq 'PTR'){
	$query .= pack('H*','00000c0001'); 
}
$sock->send($query);

# HANDLE RESPONSE
$sock->recv($datagram,1024);
($numquestions,$numanswers,$numauthority) = unpack('n n n',substr($datagram,4,6));

#print("\nQuestions: $numquestions\nAnswers: $numanswers\nAuthority: $numauthority\n");

if($numauthority > 0){
	print("Error, you got authority answers, this may mean there's a problem\n");
}

$index = 12;

# Now we have to step through the questions and answers because they are variable length
$pad = pack('B8','00000000');
# QUESTIONS
for($i=0;$i<$numquestions;$i++){
	# Again, no way to unpack just 8bits into a number, so we have to fake it
	$bytes = $pad . substr($datagram,$index,1);
	$index++;
	$llen = unpack('n',$bytes);
	while($llen > 0){
		$label = unpack('a*',substr($datagram,$index,$llen));
		$index += $llen;
#		print("label: $label\n");
		$bytes = $pad.substr($datagram,$index,1);
		$index++;
		$llen = unpack('n',$bytes);
	}
	# skip Type A and Class IN
	$index+=4;
}

# ANSWERS

for($i=0;$i<$numanswers;$i++){
	$index+=2; # skip Name field (whatever that's for)
	$type = unpack('n',substr($datagram,$index,2));
	$index+=2;
#	print("Type: $type\n");
	if($type==5){  # CNAME
		$index+=2; # Class: IN
		$index+=4; # TTL
		# two byte data length
		$ans_len = unpack('n',substr($datagram,$index,2));
		$index+=2;
#		print("answer len: $ans_len\n");
		$bytes = $pad . substr($datagram,$index,1);
		$index++;
		$llen = unpack('n',$bytes);
#		print("label len: $llen\n");
		$label = unpack('a*',substr($datagram,$index,$llen));
		print("CNAME: $label\n");
		$index+=$llen;
		$index += 2; # not real sure what these bytes refer to.
		## TODO, I think it's a link back to the domain label, see PTR code below
	}elsif($type==1){ # A record
		$index+=2; # Class: IN
		$index+=4; # TTL
		$ans_len = unpack('n',substr($datagram,$index,2));
		$index+=2;
		# what does this look like for v6?
		if($ans_len == 4){
			@octets = ();
			for($i=0;$i<$ans_len;$i++){
				$bytes = $pad . substr($datagram,$index,1);
				$index++;
				$a = unpack('n',$bytes);
				push(@octets,$a);
			}
			print("A: ",join(".",@octets),"\n");
		}
	}elsif($type==12){
		$index+=2; # Class: IN
		$index+=4; # TTL
		# two byte data length
		$ans_len = unpack('n',substr($datagram,$index,2));
		$index+=2;

		$bytes = $pad . substr($datagram,$index,1);
		$index++;
		$llen = unpack('n',$bytes);
		@labels = ();
		while($llen > 0){
			if($llen == 192){
				# I think this is a link to a previous label
				$bytes = $pad . substr($datagram,$index,1);
				$index++;

				## process previous label index
				$p_index = unpack('n',$bytes); #previous label index
				$bytes = $pad . substr($datagram,$p_index,1);
				$p_index++;
				$llen = unpack('n',$bytes);
				while($llen > 0){
					$label = unpack('a*',substr($datagram,$p_index,$llen));
					push(@labels,$label);
					$p_index+=$llen;
					$bytes = $pad . substr($datagram,$p_index,1);
					$p_index++;
					$llen = unpack('n',$bytes);
				}
			}else{

				$label = unpack('a*',substr($datagram,$index,$llen));
				push(@labels,$label);
#			print("PTR: $label\n");	
#		$index+=$llen;
				$index+=$llen;
				$bytes = $pad . substr($datagram,$index,1);
				$index++;
				$llen = unpack('n',$bytes);
			}
		}
		print("PTR: ",join(".",@labels),"\n");
#		$index+=2;  #end bytes

	}else{
		print("Error, unknown answer type: $type\n");
	}

}

close($sock);

}

exit(1);
## UNUSED
$query = pack('B8','10000001');  # transaction ID
$query .= pack('B8','01010000'); # transaction ID
$query .= pack('B8','00000001'); # Flags: standard query
$query .= pack('B8','00100000'); # Flags
$query .= pack('B8','00000000'); # Questions
$query .= pack('B8','00000001'); # Questions 1
$query .= pack('B8','00000000'); # Answer RRs
$query .= pack('B8','00000000'); # Answer RRs
$query .= pack('B8','00000000'); # Authority RRs
$query .= pack('B8','00000000'); # Authority RRs
$query .= pack('B8','00000000'); # Additional RRs
$query .= pack('B8','00000000'); # Additional RRs 0
$query .= pack('B8','00000000'); # Query end

$query .= pack('B8','00000000'); # Type
$query .= pack('B8','00001100'); # Type PTR
$query .= pack('B8','00000000'); # Class
$query .= pack('B8','00000001'); # Class IN

print(unpack("H*",$query));

$query .= pack('B8','00000000'); # RR OPT
$query .= pack('B8','00000000'); # 
$query .= pack('B8','00101001'); #
$query .= pack('B8','00010000'); #
$query .= pack('B8','00000000'); # 
$query .= pack('B8','00000000'); # 
$query .= pack('B8','00000000'); # 
$query .= pack('B8','00000000'); # 
$query .= pack('B8','00000000'); # 
$query .= pack('B8','00000000'); # 
$query .= pack('B8','00000000'); # 


