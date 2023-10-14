import fs from "fs";
import path from "path";
import matter from "gray-matter";
import {remark} from "remark";
import html from "remark-html";

const postsDirectory=path.join(
	process.cwd(),"pages/posts"
);

export function getPostsIds() {
	const fileNames=fs.readdirSync(postsDirectory).filter((fileName)=>
		fileName.endsWith(".md")
	);
	// objcomp ::: return { return {key: value} }
	return fileNames.map((fileName)=>{
		return {params: {id: fileName.replace(".md","")}}
	});
}

export function getPostsSpec() {
	// Extracts title, date, and id from each posts
	const fileNames=fs.readdirSync(postsDirectory).filter((fileName)=>
		fileName.endsWith(".md")
	);
	const postsMatter=fileNames.map(
		(fileName)=>{
			const id=fileName.replace(".md","");
			const fullPath=path.join(postsDirectory,fileName);
			const fileData=fs.readFileSync(fullPath,"utf8");
			const fileMatter=matter(fileData);
			return {id,...fileMatter.data};
		}
	);
	return postsMatter.sort(
		(q,w)=>{
			const isLater=q.date<w.date;
			const isLaterResult=isLater?1:-1;
			return isLaterResult;
		}
	);
}

export async function getPostData(id) {
	const postFilePath=path.join(postsDirectory,`${id}.md`);
	const postData=fs.readFileSync(postFilePath,"utf8");
	// matter(mkDownFileData) returns x.data
	const postMatter=matter(postData);
	const postRemk=await remark()
		.use(html)
		.process(postMatter.content);
	const postHtml=postRemk.toString();
	// postId, postHtml, postSpec
	return {id,postHtml,...postMatter.data};
}

