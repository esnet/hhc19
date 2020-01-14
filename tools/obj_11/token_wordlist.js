var Chance = require('chance');
const fs = require('fs') 

const getTestFlag = seed => {
   const chance = new Chance(seed);
   return chance.string({
       length: 8,
       pool: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
   });
} 

// https://crate.elfu.org/css/styles.css/0 -> 2AQ2PZM0
// As verified by: $ curl 'https://crate.elfu.org/unlock' -H 'Content-Type: application/json'
//                    --data '{"seed":"0","id":"9","code":"2AQ2PZM0"}'
// {"9":true}

var uuid = "7b5a647b-1b41-4973-bc38-4472c3ee484a";
var charset = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~";

// First one was `_ls`, so we'll narrow the search space
var charset = " abcdefghijklmnopqrstuvwxyz";

function toRadix(N,radix) {
    var HexN = "", 
        Q = Math.floor(Math.abs(N)), 
        R,
        strv = charset,
        radix = strv.length;
    while (true) {
        R = Q % radix;
        HexN = strv.charAt(R) + HexN;
        Q = (Q - R) / radix; 
        if (Q == 0) 
            break;
    };
    return ((N < 0) ? "-" + HexN : HexN);
};


function crack(flags){

    var index = 0;
    
    fs.readFileSync("wordlist.txt").toString().split("\n").forEach(function(line, index, arr) {
	if (index === arr.length - 1 && line === "") { return; }
	flag_index = flags.indexOf(getTestFlag(uuid + "_" + line.toLowerCase()));
        if( flag_index >= 0 )
	    console.log("Found seed for", flags[flag_index], uuid + "_" + line.toLowerCase());
    });
};

// Lock #:  1         2            3          4            5          6           7          9
crack(['F0STIHB8', 'U7VX636E', 'QO27M4Q2', 'YP68TGPC', 'XVK9EIF5', '7S4L7YC1', 'QSE47ABU', 'D6OQJZLR'], uuid);
// Seed:  console    print       <none>      ls         title       hologram    font        chakras
