module.exports = function(RED) {
	
	/////////////////////////////////////////////////////////////
	//
	//   
	//
	/////////////////////////////////////////////////////////////
	// when the connection has established 	
	//     send {"id": "<DEVICE_NAME>"} 
	// send every message from the server to the output
	// send every input message to the server 
	/////////////////////////////////////////////////////////////
	
    function MagentaConnector(config) {
		var net = require('net'); //https://nodejs.org/api/net.html
		let socket = new net.Socket()

		this.host = config.host || null;
		this.port = config.port * 1;
		this.device = config.device;
		
        RED.nodes.createNode(this,config);

		msg = {"topic":this.topic, "payload":""};

        var node = this;
		var started = false;
		
		node.log("Initializing " + config.name);
		node.log("host=" + config.host);
		node.log("port=" + config.port);
		node.log("device=" + config.device);

		options = {
			"port": config.port,
			"host": config.host
		};
		
		socket.setEncoding('utf8');
		node.status({fill:"white",shape:"dot",text:""});


		// connect to Magenta Skill Server
		function Connect() {
			node.status({fill:"yellow",shape:"dot",text:"connecting"});
			if (node.debug === 'all') node.warn('Data received from ${socket.remoteAddress}:${socket.remotePort}');
			node.log("connecting to " + options.host + " port " + options.port);
			socket.connect(options);
		}
	
		// reconnect again in few seconds
		function Reconnect(mseconds = 5000) {
			node.log('Reconnect in ' + mseconds + " ms")
			setTimeout(Connect, mseconds);
		}
		
		function SendHelloServer() {
			// todo need to escape ' in config.device
			line = '{"id": ' + config.device + '}';
			TcpSend(line);
		}

		socket.on('error', function(err) {
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
				socket.write(text + "\n");
			} else {
				node.log('not connected. Ignored: ' + text);
			}			
		}

		// response received from a node, send it back to the Skill Server
        node.on('input', function(newmsg) {
			msg = newmsg;
            node.log("imput: " + JSON.stringify(msg));			
			TcpSend(msg.payload);
        });

		node.on("close",function() {
			node.log("node close");	
			node.status({fill:"red",shape:"dot",text:"disconnected"});			
		})
			
		Connect();			
    }
	
    RED.nodes.registerType("magenta-connector",MagentaConnector);
	
}
