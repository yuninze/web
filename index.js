// common librires
const express=require("express")
const path=require("path")
const rateLimit=require("express-rate-limit")
const favicon=require("serve-favicon")
const fs=require("node:fs")

// external libraries
const Stream=require("node-rtsp-stream")

// innermost declares
const server=express()
const port=80
const root="c:/code/web/"

const assert=(indent)=>{
	let datetime=new Date()
	datetimeString=datetime.toISOString().split(".")[0].replace("T",": ")
	return " ".repeat(indent) + datetimeString + ": "
}

const camData=JSON.parse(fs.readFileSync("../cam.json"))
const cam=camData.camera.map((cam)=>{
		return [
			cam.name,
			camData.protocol+"://"+camData.account+"@"+camData.internAddress+cam.channel+camData.addressSuffix
		]
	})
const Streaming=()=>{
	return cam.map((camEach)=>{
		return new Stream({
			name:camEach[0],
			streamUrl:camEach[1],
			wsPort:90+cam.indexOf(camEach),
			ffmpegOptions:{
				'-r':24,
				'-loglevel':'warning',
				'-nostats':''
			}
		})
	})
}
let camStream=Streaming()
setTimeout(()=>{
	camStream.map((camStream)=>{camStream.stop()})
	camStream=Streaming()
},60000 * 10)

const limiter=rateLimit({
	windowMs:10 * 60000,
	max:100
})

server.use(express.json())
server.use(express.urlencoded({extended:true}))
server.use(limiter)
server.use(favicon(root + "favicon.ico"))

const sessionInfo=[]
let message={"method":null,"about":null}

const messaging=(indent,message)=>{
	const {method,about}=message
	if (method=="LOW") {
		msg=assert(indent) + `${method}: ${about}`
	} else { 
		msg=assert(indent) + sessionInfo.ip + ": " + sessionInfo.ua + ": " + `${method}: ${about}`
	}
	console.log(msg)
}

server.use((req,res,next)=>{
	sessionInfo.ip=req.headers["x-forwarded-for"] || req.socket.remoteAddress
	sessionInfo.ua=req.get("User-Agent")
	
	if (req.method=="GET") {
		let fileName=req.originalUrl
		message.method="GET"
		message.about=fileName
		if (sessionInfo.ua==false) {
			message.about+=" (dropped)"
			messaging(2,message)
			res.end()
		}
	} else if (req.method="POST") {
		message.method="POST"
	} else {
		message.method="UNKNOWN"
	}
	
	messaging(2,message)
	next()
})

server.get("/",(req,res)=>{
	res.end()
})

server.get("*",(req,res)=>{
	res.sendFile(path.join(__dirname,fileName))
})

server.post("/send",(req,res)=>{
	console.dir(req.body)
	messaging(3,message)
	res.send("got: ")
})

server.listen(port,()=>{
	message.method="LOW"
	message.about="..."
	messaging(1,message)
})
