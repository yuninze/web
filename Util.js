exports.ima=()=>{
	let date=new Date()
	return date.toISOString().split(".")[0]
}