import {
	A,Header,WitChoc,BigBoldLetters,ShowThe
} from "../front.js";
import {
	getPostsIds,getPostData
} from "../back.js";
import styleOf from "../../components/styleOf.module.css";

export async function getStaticPaths() {
	const paths=getPostsIds();
	// paths (mapped object of id strings)
	return {paths,fallback: false};
}

export async function getStaticProps({params}) {
	const postData=await getPostData(params.id);
	return {props: {postData}};
}

export default function Post({postData}) {
	return (
		<>
			<Header title={[postData.id]}/>
			<WitChoc/>
			
			<div className={styleOf.post}>
				{postData.title} {postData.date}
				<hr />
				<div dangerouslySetInnerHTML={{__html: postData.postHtml}}/>
				<span>A page ({postData.id}) based on dynamic routing.</span>
			</div>
		</>
	);
}