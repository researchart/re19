//import relevant database modules (sqlite3)
const sqlite3 = require('sqlite3').verbose();

//customLogger currently fails to record the seed for the bot message
class CustomLogger {
	logActivity(activity) {
		if (!activity) { 
	        throw new Error('Activity is required.'); 
	    }
	    // tslint:disable-next-line:no-console
        //Activate following statement to log every activity to console
        //console.log('Activity Log:', activity);

        //Comence writing data to sqlite3 database
        //Create database object
        //eli.db for testing, prepreTest.db for prepreTest
        let db = new sqlite3.Database('./data/eli.db', (err) => {
            if (err) {
                return console.error(err.message);
            }
            console.log('Database// Connected to in-memory sqlite database.') 
        });

        //attempt to serialize all functionality in the following:
        db.serialize(function() {

        	function wrapperFunction(cb) {
	        	db.serialize(function() {
					//retrieve latest messageID and latest seed
					let seed = '';

					//retrieve seed first
					let sql = `SELECT seed FROM chains WHERE conversationID = ? AND recipient = 'LadderBot' ORDER BY timestamp DESC LIMIT 1`;
			        let params = activity.conversation.id;

			        db.get(sql, params, (err, row) => {
				        	if(err) {
				                return console.error(err.message);
				            }

				            if(typeof(row) != 'undefined') {
				            	if(row.seed === null) {
				            		seed = 'undefined';
				            	} else {
				            		//return latest seed
				            		seed = row.seed;
				            	}
				            }
				            else {
				            	seed = 'undefined';
				            }
			        });

			        //then retrieve messageID

			        sql = `SELECT messageID FROM chains WHERE conversationID = ? ORDER BY messageID DESC LIMIT 1`;
			        params = activity.conversation.id;

			        db.get(sql, params, (err, row) => {
				        	if(err) {
				                return console.error(err.message);
				            }

				            if(typeof(row) != 'undefined') {
				            	if(row.messageID === null) {
				            		return cb(1, seed);
				            	} else {
				            		//return latest messageID and increase by 1
				            		return cb((row.messageID + 1), seed);
				            	}
				            }
				            else {
				            	return cb(1, seed);
				            }
			        });
	        	});
	        }

	        //perform an logging activity if the message received is from the bot
	        if(activity.type == 'message' && activity.from.name == 'LadderBot') {
	        	//get values from serialized callback function to ensure async working (x = messageID, y = seed)
		        wrapperFunction((x, y) => {
		        	//set parameters for writing activity to DB
		        	console.log('//Bot - latestMessageID: ' + x);

			        let sql = 'INSERT INTO chains VALUES(?,?,?,?,?,?,?)';
			        let params =[activity.conversation.id, y, activity.from.name, activity.recipient.name, activity.text, x, activity.timestamp];

			        db.run(sql, params, function(err) {
			            if(err) {
			                return console.error(err.message);
			            }
		        	});

		        	//Terminate database connection
		        	db.close((err) => {
			            if(err) {
			                return console.error(err.message);
			            }
		            console.log('Database// Terminate in-memory sqlite database connection.')
		        	}); 
		        });

	        }

	        //perform a logging activity if the message retrieved is from a human user
	        else if(activity.name == 'newUserInput') {
		        wrapperFunction((x, y) => {
		        	//set parameters for writing activity to DB
			        let sql = 'INSERT INTO chains VALUES(?,?,?,?,?,?,?)';
			        let params =[activity.conversation.id, activity.value[1], 'ClientUserName', 'LadderBot', activity.value[0], x, activity.timestamp];

			        db.run(sql, params, function(err) {
			            if(err) {
			                return console.error(err.message);
			            }
		        	});

		        	//Terminate database connection
		        	db.close((err) => {
			            if(err) {
			                return console.error(err.message);
			            }
		        	}); 
		        });
	        
	        } else {
	        	//Insert comment if skipped
	        }
        });
     
	}
}
exports.CustomLogger = CustomLogger;