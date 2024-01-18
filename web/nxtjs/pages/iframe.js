import A from "next/link"
import {WitChoc} from "./front.js"
import styleOf from "../components/styleOf.module.css"

const cameras=[
{
name:"개스통",
address:"rtsp://admin:kx87dnm2@211.228.185.97:10000/1/2",
addressSecondary:"rtsp://admin:kx87dnm2@172.30.1.1/1/2"
},
{
name:"현관",
address:"rtsp://admin:kx87dnm2@211.228.185.97:10001/1/2",
addressSecondary:"rtsp://admin:kx87dnm2@172.30.1.2/1/2"
},
{
name:"길가",
address:"rtsp://admin:kx87dnm2@211.228.185.97:10002/1/2",
addressSecondary:"rtsp://admin:kx87dnm2@172.30.1.3/1/2"
},
{
name:"뒷쪽",
address:"rtsp://admin:kx87dnm2@211.228.185.97:10003/1/2",
addressSecondary:"rtsp://admin:kx87dnm2@172.30.1.4/1/2"
}
]

function CamerasLinks() {
	return (
		<div className={styleOf.container}>
			{cameras.map(camera=>(
				<p key={camera.name}>
					<A href={camera.address}><b>{camera.name}</b></A>
					<A href={camera.addressSecondary}><b> (Alternative)</b></A>
				</p>
			))}
		</div>
	)
}

export default function IFrameScreen() {
	return (
		<>
			<WitChoc/>
			<CamerasLinks/>
		</>
	)
}