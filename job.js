const extractExt=(filenameString)=>{
	const filenameStringBooleanVector=Array.from(filenameString).map(char=>char===".")
	const extDotPosition=filenameStringBooleanVector.findLastIndex(vector=>vector===true)
	return extDotPosition
}

const nikki=(datetime,ip,ua,method,path)=>{
	const nikkiStream=fs.createWriteStream(
		"./nikki.csv",
		{flags:"a"}
	)
	nikkiStream.write(
		`"${datetime}","${ip}","${ua}","${method}","${path}"\n`
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