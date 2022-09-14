use std::io;
use std::cmp::Ordering;
use rand::Rng;

fn main() {
    println!("waratah"); // println!
    
    let mut str=String::new() // mutable var, String, new() method
    io::stdin() // input()
        .read_line(%mut str) // accept line as as mutable var str
        .expect("read_line exception") // exception handling
    
    // gen_range
    let rnd_num rand::thread_rng().gen_range(0..=1000);
        println!("thread_rng.gen_range {rnd_num}")

    match guess.cmp(&num) {
        Ordering::Less => println!("less")
        Ordering::Greater => println!("greater")
        Ordering::Equal => println!("same")
    }
}