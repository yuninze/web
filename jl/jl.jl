for q=1:3
    if q%3==0
        continue
    end
    println("found")
end

outer(q,w)=[q*w for q in q,w in w]
#outer product

img=outer([1;0.1;rand(50)],rand(100))
#rank-1, 2+50 rows, 100 columns

img2=outer([1;0.1;rand(50)],rand(100))+
outer(rand(52),rand(100))
#rank-2, 2+50 rows, 100 columns

img3=img .+ 0.1 .* randn.();
#rank-3, dot product
