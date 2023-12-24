#### Convention
1. import x from {}
2. /x.jpg => ./public/x.jpg
3. ../ => 그 페이지의 ../
4. export {f,h,g}; => import {f,h,g} from "module";
5. [Reference](https://airbnb.io/javascript/react/)

#### Node.js
1. Node.js
2. Create Repo. Directory

#### npm => Next.js
1. Create a file named package.json with {}
2. .../ 
3. npm install react react-dom next remark gray-matter
4. package.json에 dependencies.. npm install

#### 앱 작성
1. Create a folder named pages
2. npx create-next-app@latest {name} --use-npm
> npx create-next-app@latest nextjs-blog --use-npm --example "https://github.com/vercel/next-learn/tree/main/basics/learn-starter"
3. npm run dev

#### git on commandline
##### repo path
- git remote show origin
- git remote get-url origin
- git remote -v

##### set repo path
- git remote set-url origin https://github.com/yuninze/yeonsup

##### fetch
- git fetch

##### pull
- git pull origin master

##### set target files in repo
- git add .
- git diff
- git status -z -uall

##### commit
- git commit -m "git:cmd"
- git push origin master