const http=require("node:http")
const url=require("url")
const fs=require("fs")

const Util=require("./Util")
const Stream=require("node-rtsp-stream")

const hostname="172.30.1.18"
const hostpath="http://"+hostname
const port=80
const mainPage="./main.html"
const assert=". ".repeat(3)

const camData=JSON.parse(fs.readFileSync("../camera.json"))
const cams=camData.camera.map(
	(cam)=>{
		return [
			cam.name,
			camData.protocol+"://"+camData.account+"@"+camData.internAddress+cam.channel
		]
	}
)
const camStreams=cams.map(
	(cam)=>{
		return new Stream({
			name:cam[0],
			streamUrl:cam[1],
			wsPort:90+cams.indexOf(cam),
			ffmpegOptions:{
				'-r':24,
				'-loglevel':'info',
				'-nostats':''
			}
		})
	}
)

const server=http.createServer(
	(req,res)=>{
		const sendContent=(title,content)=>{
			res.writeHead(200,{"Content-Type": "text/html; charset=utf-8"})
			res.write(`
				<html>
					<head>
						<title>${title}</title>
					</head>
					<body>
						<section>
							<h1>${title}</h1>
							<h4>${content}</h4>
							<a href=${mainPage}><h1>Go Back</h1></a>
						</section>
					</body>
				</html>
			`,"utf-8")
		}
		
		let filePath
		if (req.url.length>1) {
			filePath="."+new URL(hostpath+req.url).pathname
		} else {
			filePath=mainPage
		}
		
		console.log(assert+filePath)
		
		fs.readFile(filePath,
			(error,data)=>{
				if (error) {
					console.log(assert.repeat(2)+error)
					sendContent("There was an error",error.toString().replace("Error: ",""))
					return res.end()
				}
				
				let fileContentType
				if (filePath.endsWith(".html")) {
					fileContentType="text/html"
				} else if (filePath.endsWith(".js")) {
					fileContentType="text/javascript"
				} else { 
					fileContentType=false
				}
				
				if (fileContentType===false) {
					sendContent("There was an error","Unknown File Content Type")
					return res.end()
				}	
				
				res.writeHead(200,{
					"Content-Type": fileContentType+"; charset=utf-8",
				})
				res.write(data,"utf-8")
				return res.end()
			}
		)
	}
)

server.listen(port,hostname,
	()=>{
		console.log(`${assert}Running at ${hostname}:${port} from ${Util.ima()}`)
	}
)