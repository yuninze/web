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
- git remote show origin
- git remote set-url origin https://github.com/yuninze/yeonsup
- git remote get-url origin
- git remote -v
- git status -z -uall
- git fetch
- git status -z -uall
- git diff
- git pull origin master
- git commit
- git push -u origin master