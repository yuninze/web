/* Server-side properties */

import fs from "fs";
import path from "path";
import matter from "gray-matter";

const postsDirectory=path.join(
	process.cwd(),"pages/posts"
);

export function getPostsMatter() {
	const filenames=fs.readdirSync(postsDirectory);
	const postsMatter=filenames.map(
		(filename)=>{
			const id=filename.replace(".md","");
			const fullPath=path.join(postsDirectory,filename);
			
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
