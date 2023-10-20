export default function handler(req,res) {
	const Content=[
		{name:"string",type:"q"},
		{name:"coffee",type:"q"},
	]
	res.status(200).json(Content)
}