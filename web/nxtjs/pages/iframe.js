import {WitChoc} from "./front.js"

export default function IFrameScreen() {
	return (
		<>
			<WitChoc/>
			<iframe src="https://www.google.com/webhp?igu=1" width={1200} height={1080}></iframe>
		</>
	)
}