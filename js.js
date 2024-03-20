const path=require("path")
const fs=require("node:fs")
const Papa=require("papaparse")

const Stream=require("node-rtsp-stream")
const cams=JSON.parse(fs.readFileSync("../camData.json"))
const cam=cams.cam.map(
	(cam)=>{
		return [
			cam.name,
			cams.protocol+'://'+cams.account+'@'+cams.internAddress+cam.channel+cams.addressSuffix
		]
	})

const loadStreams=()=>{
	return cam.map((camEach)=>{
		return new Stream({
			name:camEach[0],
			width:704,
			height:480,
			streamUrl:camEach[1],
			wsPort:90+cam.indexOf(camEach),
			ffmpegOptions:{
				"-r":24,
				"-loglevel":"warning"
			}
		})
	})
}
const camStreams=loadStreams()

const express=require("express")
const favicon=require("serve-favicon")
const server=express()
const port=80
const root="c:/code/web/"
const rootPage="/"
const uploadRoot="./upload/"

const rateLimit=require("express-rate-limit")
const limiter=rateLimit({
	windowMs:1 * 2000,
	max:10,
	message:async(req,res)=>{
		message.method=req.method
		message.about="BLOCKED"
		messaging(3,message)
		return errorPage("It's done","Reached limit")
	}
})

const multer=require("multer")
const disk=multer.diskStorage({
	destination:(req,file,q)=>{
		q(null,uploadRoot)
	},
	filename:(req,file,q)=>{
		let extDotPosition=extractExt(file.originalname)
		let name
		let ext
		if (extDotPosition>0) {
			name=file.originalname.slice(0,extDotPosition)
			ext=file.originalname.slice(extDotPosition)
		} else {
			name=file.originalname
			ext=""
		}
		let filename=req.body.idx+"_"+req.body.proofType+"_"+Date.now()+ext
		q(null,filename)
	}
})
const upload=multer({storage:disk})

const assert=(indent=0)=>{
	let datetime=new Date()
	datetimeString=datetime.toISOString().split(".")[0].replace("T",": ")
	return " ".repeat(indent) + datetimeString
}

const extractExt=(filenameString)=>{
	const filenameStringBooleanVector=Array.from(filenameString).map(char=>char===".")
	const extDotPosition=filenameStringBooleanVector.findLastIndex(vector=>vector===true)
	return extDotPosition
}

const writeNikki=(datetime,ip,ua,method,path)=>{
	const nikki=fs.createWriteStream(
		"./nikki.csv",
		{flags:"a"}
	)
	nikki.write(
		`"${datetime}","${ip}","${ua}","${method}","${path}"\n`
	)
}

let sessionInfo=new Array()
let message={"method":null,"about":null}
const messaging=(indent,message)=>{
	const {method,about}=message
	if (method=="LOW") {
		msg=assert(indent) + ": " + `${method}: ${about}`
	} else { 
		msg=assert(indent) + ": " + `${sessionInfo.ip}: ${sessionInfo.ua}: ${method}: ${about}`
	}
	writeNikki(assert().replace(": ","T"),sessionInfo.ip,sessionInfo.ua,method,about)
	console.log(msg)
}

const errorPage=(title,content)=>{
	const placeholderImage="error.png"
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
				<a href=${rootPage}><h2>Go Back</h2></a>
			</div>
		</body>
	</html>
	`)
}

server.use(express.static("./res"))
server.use(limiter)
server.use(favicon("./res/favicon.ico"))

server.use((req,res,next)=>{
	sessionInfo.ip=req.headers["x-forwarded-for"] || req.socket.remoteAddress
	sessionInfo.ip=sessionInfo.ip.slice(sessionInfo.ip.indexOf(":",2)+1)
	sessionInfo.ua=req.get("User-Agent")
	
	if (req.method=="GET") {
		message.method="GET"
		message.about=req.originalUrl
		
		if (sessionInfo.ua==false || req.originalUrl.length<3 || req.originalUrl.endsWith("php")) {
			message.about+=" (dropped)"
			messaging(2,message)
			res.set("content-type","text/html").send(errorPage("Something went wrong","Error"))
			res.end()
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
	const reqPath=path.join(__dirname,req.originalUrl)
	
	if (fs.existsSync(reqPath)) {
		res.sendFile(reqPath)
	
	} else if (req.originalUrl==="/camStreams") {
		res.set("content-type","text/html").send(errorPage("Went wrong","Not Implemented"))
			
	} else if (req.originalUrl==="/count") {
		let files=new Promise((resolve,reject)=>{
			return fs.readdir(uploadRoot,(fail,ok)=>{
				fail != null ? reject(fail) : resolve(ok)
			})
		})
		
		files.then(f=>{
			res.status(200).json({
				content:f.length
			})
		})
	
	} else if (req.originalUrl==="/csvData") {
		const fp=fs.readFileSync("c:/code/f.csv","utf8")
		const csvData=Papa.parse(fp,{
			delimiter:",",
			headers:false
		})
		
		res.status(200).json({
			data:{
				columns:csvData.data[0],
				len:csvData.data.length-1,
				latestIndex:csvData.data[csvData.data.length-2][0]
			}
		})
		
	}	else {
		res.send(errorPage("Went wrong",`An action for '${req.originalUrl}' does not exist`))
		res.end()
	
	}
})

server.post("/uploadProof",upload.single("proofFile"),(req,res)=>{
	message.method="POST: Uploading Attempting"
	
	if (req.file) {
		message.about=`${req.file.filename} (${req.file.size})`
		res.status(200).json({content:`Uploaded: ${(req.file.size/1024).toFixed(2)}kB`})
		
	} else {
		message.about="There was an exception"
		res.status(400)
		
	}
	messaging(3,message)
	
})

server.listen(port,()=>{
	message.method="LOW"
	message.about="."
	messaging(1,message)
})
