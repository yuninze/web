include("init.jl")

typeof(12345)

string("string","concat","1234")

d=Dict("a"=>[1,2],"b"=>[3,4])
d.pop!(d,"a")
d["b"][2]==4

a=["a","b"]
push!(a,"c")
pop!(a) #removes the latest

x,y,z=(3,3,3)
rand(x,y,z) # 3x3
zeros(3,3,3) # np.zeros

n=0
while n<10
    n+=1
    println("not")
end

games=["lol","hots","ow","fallout"]
i=1
while i<=length(games)
    game=games[i]
    println("The title is $i::$game")
    i+=1
end

x=zeros(5,5)
for q in 1:size(x)[1]
    for w in 1:size(x)[2]
        x[q,w]=q+w
    end
end

for q=1:size(x)[1],w=1:size(x)[2]
    x[q,w]=q+w
end

t=[q+w for q=1:size(x)[1],w=1:size(x)[2]]

for q=games
    println(q)
end

hi(name)=println("hi $name")

for q=1:3
    if q%3==0
        continue
    end
    println("found")
end

hihi=name->println("hi hi $name $name!")
gogo= loc->println("going to $loc!")

#mutating/inplacing
v=[3,1,9]
sort(v)
sort!(v)

temps=[15,16,18,20,24,26]
mens=[100,200,3000,4000,5000,5500]
plot(mens,temps,legend=false)
scatter!(mens,temps,legend=false)
xlabel!("xlabel");ylabel!("ylabel");title!("title")
p1=plot(x,x);p2=plot(x,x.*3);p3=plot(x,x.^2);p4=plot(x,x.+10)
plot(p1,p2,p3,p4,layout=(2,2),legend=false)

@which 3+3
@which 3.0+3.0
@which 3+3.0

import Base:+
+(q::String,w::String)=string(q,w)
@which "ha"+"go"

begin
	show_image(M) = get.(Ref(ColorSchemes.rainbow), M ./ maximum(M))
	show_image(x::AbstractVector) = show_image(x')
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