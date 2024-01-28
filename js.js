const http=require("node:http")
const url=require("url")
const fs=require("fs")

const Util=require("./Util")
const Stream=require("node-rtsp-stream")

const assert=()=>{
	return ". ".repeat(2)+Util.ima()
}

const hostname="172.30.1.18"
const hostpath="http://"+hostname
const port=80
const mainPage="./main.html"
const imageInErrorPage="./biLogo.png"

const camData=JSON.parse(fs.readFileSync("../camera.json"))
const cams=camData.camera.map(
	(cam)=>{
		return [
			cam.name,
			camData.protocol+"://"+camData.account+"@"+camData.internAddress+cam.channel+camData.addressSuffix
		]
	}
)

const callStreams=()=>{
	return cams.map((cam)=>{
		return new Stream({
			name:cam[0],
			streamUrl:cam[1],
			wsPort:90+cams.indexOf(cam),
			ffmpegOptions:{
				'-r':24,
				'-loglevel':'warning',
				'-nostats':''
			}
		})
	})
}

let streams=callStreams()
setTimeout(()=>{
	streams.map((stream)=>{
		stream.stop()
	})
	streams=callStreams()
},60000 * 10)

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
							<img src=${imageInErrorPage} alt=${title}>
							<h1>${title}</h1>
							<h4>${content}</h4>
							<a href=${mainPage}><h1>Go Back</h1></a>
						</section>
					</body>
				</html>
			`,"utf-8")
		}
		
		let browser=req.headers["user-agent"]?req.headers["user-agent"]:false
		if (browser===false) {
			console.log(`${assert()} ${req.socket.remoteAddress} (${browser}) => dropped`)
			return res.end()
		}
		
		const post=(url,data)=>{
			
			console.log(`${assert()}: POST: ${req.socket.remoteAddress}: ${browser}`)
			
			const dataString=JSON.stringify(data)
			
			const options={
				method:"POST",
				headers:{
					"content-type":"application/json",
					"content-length":dataString.length
				},
				timeout:1000,
			}
		
			return new Promise((resolve,reject)=>{
				const req=http.request(url,options,
					(res)=>{
						if (res.statusCode!=200) return reject(new Error("statusCode!=200"))
						
						let body=[]
						res.on("data",(data)=>body.push(data))
						res.on("end",()=>{
							const resString=Buffer.concat(body).toString()
							resolve(resString)
						})
					})
				
				req.on("error",(error)=>{
					reject(error)
				})
				
				req.on("timeout",(timeout)=>{
					req.destory()
					reject(new Error(assert() + "Timeout"))
				})
				
				req.write(dataString)
				req.end()
			}) // promise
		}
		
		if (req.method=="GET") {
			let filePath
			if (req.url.length>1) {
				filePath="."+new URL(hostpath+req.url).pathname
			} else {
				filePath=mainPage
			}
			
			console.log(`${assert()}: GET: ${req.socket.remoteAddress}: ${browser}: ${filePath}`)
			
			fs.readFile(filePath,
				(error,data)=>{
					if (error) {
						console.log(assert()+error)
						sendContent("Something went wrong",error.toString().replace("Error: ",""))
						return res.end()
					}
					
					let fileContentType
					if (filePath.endsWith(".html")) {
						fileContentType="text/html"
					} else if (filePath.endsWith(".js")) {
						fileContentType="text/javascript"
					} else if (filePath.endsWith(".css")) {
						fileContentType="text/css"
					} else if (filePath.endsWith(".png")) {
						fileContentType="image/png"
					} else {
						sendContent("Something went wrong","Wrong Content Type")
						return res.end()
					}
					
					res.writeHead(200,{
						"Content-Type": fileContentType+"; charset=utf-8",
					})
					res.write(data,"utf-8")
					return res.end()
				}
			)
			
			if (req.method=="POST") {
				async ()=>{
					const res=await post("http://172.30.1.18/sendSomething",data)
				}
			}
			
		}
		
	}
)

server.listen(port,hostname,
	()=>{
		console.log(`${assert()}: Run at ${hostname}:${port}`)
	}
)