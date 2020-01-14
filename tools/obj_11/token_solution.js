var Chance = require('chance');
const async_request = require('request');
const sync_request = require('sync-request');

const getTestFlag = seed => {
   const chance = new Chance(seed);
   return chance.string({
       length: 8,
       pool: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
   });
} 

var uuid = "";

// First, we query the page to determine our UUID
var homepage_body = sync_request('GET', 'https://crate.elfu.org/').body.toString();
uuid = homepage_body.substr(homepage_body.indexOf('/client.js/') + 11, 36);

console.log(`UUID is ${uuid}`);

var codes = {1: getTestFlag(uuid + "_console"),
	     2: getTestFlag(uuid + "_print"),
	     3: getTestFlag(uuid),
	     4: getTestFlag(uuid + "_ls"),
	     5: getTestFlag(uuid + "_title"),
	     6: getTestFlag(uuid + "_hologram"),
	     7: getTestFlag(uuid + "_font"),
	     8: "VERONICA",
	     9: getTestFlag(uuid + "_chakras"),
	     10: "KD29XJ37"};

var body = {"seed": uuid, "codes": codes};

// Next, we try to get the JS and do the POST as close as possible.
async_request({method: 'GET', uri: `https://crate.elfu.org/client.js/${uuid}`}, (err, res, body) => {
    if (err) { return console.log("JS error" + err); }
    console.log("JS done");
});

var result = "{}";
console.log(JSON.stringify(body));
while ( result == "{}" )
{
    result = sync_request('POST', 'https://crate.elfu.org/open', {json: body}).body.toString();
    console.log(result);
}

console.log(result);


// Seed: 7f02ae0f-b423-4ce2-b392-b2d99536c36d
// 1 SGBACQ1I {'1': True}
// 2 APFVM98M {'2': True}
// 3 Q3XT8X1S {'3': True}
// 4 0A7AY4LR {'4': True}
// 5 ZTZXSLLH {'5': True}
// 6 AORH6MBE {'6': True}
// 7 ALJS2APR {'7': True}
// 8 VERONICA {'8': True}
// 9 1ATGCIB0 {'9': True}
// 10 KD29XJ37 {'10': True}
// {'seed': '7f02ae0f-b423-4ce2-b392-b2d99536c36d', 'codes': {'1': 'SGBACQ1I', '2': 'APFVM98M', '3': 'Q3XT8X1S', '4': '0A7AY4LR', '5': 'ZTZXSLLH', '6': 'AORH6MBE', '7': 'ALJS2APR', '8': 'VERONICA', '9': '1ATGCIB0', '10': 'KD29XJ37'}}


