package main

/*  Simple recursive implementation, spawns 2N goroutines
    (That's suboptimal for short tasks:
     Keeping active set to number of cores would be faster
     But I can't figure out how to limit that without `for`)

    Overview:
        split input recursively down to single integers
        compute squares 
        recombine total sum
        
        For example:
        1 + 2 + 3 + 4 becomes ((1 + 2) + (3 + 4)) // sum is associative
        and may become ((3 + 4) + (1 + 2)) // sum is commutative
        
        Variable length input:
        1 + 2 + 3 becomes (1 + (2 + 3))

    Rules assumption:
        I'll assume that `for` ban only applies to single test computation.
        That is it's OK to use `for` to iterate over tests.
        (I'm assuming test results have to be in correct order,
         thus sequential processing is justified)
*/

import (
    "os"
    "fmt"
    "bufio"
    "strings"
    "strconv"
)

func recsum(arr []string, res chan int) {
    if len(arr) == 1 {
        i, _ := strconv.Atoi(arr[0])
        if i < 0 {
            res<- 0
        } else {
            res<- i * i
        }
    } else {
        ch := make (chan int)
        mid := len(arr) / 2
        go recsum(arr[:mid], ch)
        go recsum(arr[mid:], ch)
        res<- (<-ch) + (<-ch)
    }
}

func process(file *os.File) {
    result := make (chan int)
    sc := bufio.NewScanner(file)
    sc.Scan()  // skip number of tests

    for sc.Scan() {
        sc.Scan() // skip number of integers in this test
        go recsum(strings.Split(sc.Text(), " "), result)
        fmt.Println(<-result)
    }
}

func main() {
    process(os.Stdin)
}
