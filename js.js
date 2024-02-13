const path=require("path")
const fs=require("node:fs")

const Stream=require("node-rtsp-stream")

const assert=(indent=0)=>{
	let datetime=new Date()
	datetimeString=datetime.toISOString().split(".")[0].replace("T",": ")
	return " ".repeat(indent) + datetimeString
}

const camData=JSON.parse(fs.readFileSync("../camData.json"))
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

const express=require("express")
const favicon=require("serve-favicon")
const rateLimit=require("express-rate-limit")
const multer=require("multer")

const server=express()
const port=80
const root="c:/code/web/"

const limiter=rateLimit({
	windowMs:1 * 60000,
	max:100,
	message:async(req,res)=>{
		return sendHtmlString("It's done","Reached the rate limit")
	}
})

const disk=multer.diskStorage({
	destination:(req,file,cb)=>{
		cb(null,"uploads/")
	},
	filename:(req,file,cb)=>{
		cb(null,Date.now()+"_"+file.originalname)
	}
})
const upload=multer({storage:disk})

server.use(express.json())
server.use(express.urlencoded({extended:true}))
server.use(express.static("./res"))
server.use(limiter)
server.use(favicon("./res/favicon.ico"))

let filename
let sessionInfo=new Array()
let message={"method":null,"about":null}

const nikki=(datetime,ip,ua,method,path)=>{
	const nikkiStream=fs.createWriteStream(
		"./nikki.csv",
		{flags:"a"}
	)
	nikkiStream.write(
		`${datetime},${ip},${ua},${method},${path}\n`
	)
}

const messaging=(indent,message)=>{
	const {method,about}=message
	if (method=="LOW") {
		msg=assert(indent) + ": " + `${method}: ${about}`
	} else { 
		msg=assert(indent) + ": " + `${sessionInfo.ip}: ${sessionInfo.ua}: ${method}: ${about}`
	}
	nikki(assert().replace(": ","T"),sessionInfo.ip,sessionInfo.ua,method,about)
	console.log(msg)
}

const sendHtmlString=(title,content)=>{
	const placeholderImage="error.png"
	const mainPage="/"
		return (`
		<html>
			<head>
				<meta charset="utf-8">
				<link rel="stylesheet" href="./style.css">
				<title>${title}</title>
			</head>
			<body>
				<div>
					<img src=${placeholderImage} alt=${title} width="50%">
					<h1>${title}</h1>
					<h2>${content}</h2>
					<a href=${mainPage}><h2>Go Back</h2></a>
				</div>
			</body>
		</html>
		`)
}

server.use((req,res,next)=>{
	sessionInfo.ip=req.headers["x-forwarded-for"] || req.socket.remoteAddress
	sessionInfo.ip=sessionInfo.ip.slice(sessionInfo.ip.indexOf(":",2)+1)
	sessionInfo.ua=req.get("User-Agent")
	
	if (req.method=="GET") {
		filename=req.originalUrl
		message.method="GET"
		message.about=filename
		
		if (sessionInfo.ua==false || filename.length<3 || filename.endsWith("php")) {
			message.about+=" (dropped)"
			messaging(2,message)
			res.set("content-type","text/html")
			res.send(sendHtmlString("Something went wrong","Error"))
			return res.end()
		}
		
	} else if (req.method="POST") {
		message.method="POST"
		message.about=req.originalUrl
	
	} else {
		message.method="UNKNOWN"
		message.about="*"
	}
	
	messaging(2,message)
	next()
})

server.get("*",(req,res)=>{
	const reqPath=path.join(__dirname,filename)
	if (fs.existsSync(reqPath)) {
		res.sendFile(reqPath)
	} else {
		res.send(sendHtmlString(
			"Something went wrong",
			`'${filename}' does not exist`
		))
		return res.end()
	}
})

server.post("/upload",upload.single("file"),(req,res)=>{
	if (req.file) {
		const filename=req.file.filename
		message.method="POST: UPLOAD"
		message.about=filename
		res.status(200).json({"success":true,"filename":filename})
	} else if (!req.file) {
		res.status(400).send(`This POST req. is likely null`)
	}
	messaging(3,message)
})

server.listen(port,()=>{
	message.method="LOW"
	message.about="..."
	messaging(1,message)
})
