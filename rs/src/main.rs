use std::collections::HashMap;
use std::collections::HashSet;
fn borrowing_only(some_string:&String){
    println!("{}",some_string);
}
fn calculate_len(some_string:&String)->usize{
    some_string.len()
}
fn slice_stat(some_slice:&[i64]){
    let some_slice_len=some_slice.len();
    println!("{:?} is {some_slice_len} long",some_slice);
}
#[derive(Debug)] // dec for println
enum Sbckstype{
    Drip,Essp,Pucci,Fizzio,Event
}
struct Sbcks{
    name:Sbckstype, // enum
    price:i64,
    favor:bool
}
impl Sbcks{
    fn doge(&self)->i64{
        self.price*2
    }
}
fn sbcks_menu(sbcks:Sbcks){
    println!("{:?} is {} won {}",{sbcks.name},{sbcks.price},{sbcks.favor});
}
fn main(){
    // String::from==py::str()
    let mut some_string=String::from("peppi");
    // borrowing object
    borrowing_only(&some_string);
    println!("{}",some_string);
    let some_string_len=calculate_len(&some_string);
    println!("{some_string} is {some_string_len} char long");
    // referring occured for sames
    let mut some_string_mutable=&mut some_string;
    let some_string_len_two=&some_string_len;
    // array accepts only one data type
    let mut fizzio=[6,9,0,0];
    slice_stat(&fizzio);
    // tuple accepts various data types
    let sbuck=("fizzio","6900","lime");
    println!("{}.. is {}.. much {}.. taste",sbuck.0,sbuck.1,sbuck.2);
    // struct
    let fizzio=Sbcks{
        name:Sbckstype::Drip,
        price:6900,
        favor:false
    };
    let pucci=Sbcks{
        name:Sbckstype::Pucci,
        price:5700,
        favor:false
    };
    // struct method
    let domyung_price=fizzio.doge();
    let fizzio_name=&fizzio.name;
    // borrows domyung_price
    println!("{:?} 두 개 가격은 {}",fizzio_name,&domyung_price);
    sbcks_menu(pucci);
    // Vector is a listlike object can be shrinked, appended
    let mut vektor=Vec::new();
    for q in 0..5 {
        let w=&q;
        vektor.push(q);
        println!("벡터에 {q} 추가함")
    }
    vektor.remove(4);
    println!("벡터에서 지움");
    if vektor.contains(&0)==true {
        println!("vector contains something");
    }
    let vektor_length=vektor.len();
    println!("벡터 길이: {}",&vektor_length);
    println!("벡터 모양: {:?}",&vektor);
    let mut vektor_=vec![0,1,2];
    // HashMap is dict
    let mut dict=HashMap::new();
    dict.insert("sbucks","fizzio");
    let sbucks_menu=dict.get(&"sbucks");
    for (key,val) in dict.iter() {
        println!("{key}, {val}");
    }
    let mut hs_=HashSet::new();
    hs_.insert("test");
    hs_.len();

}