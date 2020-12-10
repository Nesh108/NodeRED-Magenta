module.exports = function(RED) {
	
	/////////////////////////////////////////////////////////////
	//
	//    Magenta Connector node-red node   
	//    2020-12-08 Reinhard Henning
	//
	/////////////////////////////////////////////////////////////
	// what it does:
	// This node connects to a server via TCP specified in host port
	// when the connection has established: 	
	//     send json string {"id": "<DEVICE_NAME>"} 
	// every message from the server is send to the node output
	// every input message is send back to the server 
	/////////////////////////////////////////////////////////////
	
    function MagentaConnector(config) {
		var net = require('net'); //https://nodejs.org/api/net.html
		let socket = new net.Socket()

		this.host = config.host || null;
		this.port = config.port * 1;
		this.device = config.device;
		this.topic = config.topic;
		
        RED.nodes.createNode(this,config);

		msg = {};
		timer = {};
	
        var node = this;
		var started = false;
		
		node.log("Initializing " + config.name);
		node.log("host=" + config.host);
		node.log("port=" + config.port);
		node.log("device=" + config.device);
		node.log("topic=" + config.topic);

		options = {
			"port": config.port,
			"host": config.host
		};
		
		socket.setEncoding('utf8');
		node.status({fill:"white",shape:"dot",text:""});


		// connect to Magenta Skill Server
		function Connect() {
			node.status({fill:"yellow",shape:"dot",text:"connecting"});
			node.log("connecting to " + options.host + " port " + options.port);
			socket.connect(options);
		}
	
		// reconnect again in few seconds
		function Reconnect(mseconds = 10000) {
			node.log('clear timeout');
			clearTimeout(timer);
			node.log('Reconnect in ' + mseconds + " ms")
			timer = setTimeout(Connect, mseconds);
		}
		
		function SendHelloServer() {
			// todo need to escape ' in config.device
			node.log('Sending device-ID');
			line = JSON.stringify({ "id": config.device});
			TcpSend(line);
		}

		socket.on('error', function(err) {
			//socket.destroy();
			node.log('socket error ' + err.code);			
			node.status({fill:"red",shape:"dot",text:"disconnected"});
			Reconnect();
		});

		socket.on('connect', function() {
			node.log('connection established');			
			SendHelloServer();
			node.status({fill:"green",shape:"dot",text:"connected"});
		});
		
		socket.on('data', function(data) {
			node.log('data received: ' + data);
			msg.payload = data;
			node.send(msg);
		});
		
		function TcpSend(text) {
			if (socket.readyState == "open") {
				node.log('sending back: ' + text);
				socket.write(text + "\n");
			} else {
				node.log('not connected. Ignored: ' + text);
			}			
		}

		// response received from a node, send it back to the Skill Server
        node.on('input', function(msg) {
			if (config.topic != "") {
				// we have configured to override the topic 
				msg.topic = config.topic;
			};
			
            node.log("imput: " + JSON.stringify(msg));			
			TcpSend(msg.payload);
        });

		node.on("close",function() {
			node.status({fill:"red",shape:"dot",text:"disconnected"});
			node.log("node close");	
			clearTimeout(timer);
			socket.end();		
            socket.destroy();
            socket.unref();			
		})
		
		node.log("ready");	
		Connect();			
    }
    RED.nodes.registerType("magenta-connector",MagentaConnector);
}