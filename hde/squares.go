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
        I'll assume that `for` ban only apply to single test computation.
        That is        it's OK to use `for` to iterative over tests.
*/

import (
        "fmt"
        "strings"
        "strconv"
)

func recsum(arr []string, res chan int) {
        if len(arr) == 1 {
                i, _ := strconv.Atoi(arr[0])
                if i < 0 {
                        res <- 0
                } else {
                res <- i * i
                }
        } else {
        ch := make (chan int)
        mid := len(arr) / 2
        go recsum(arr[:mid], ch)
        go recsum(arr[mid:], ch)
        res<- (<-ch) + (<-ch)
        }
}

func main() {
        fmt.Println("Hello, playground")
        data := "3 -1 1 14"
        inp := strings.Split(data, " ")
        fmt.Println(inp)

        result := make (chan int)
        go recsum(inp, result)
        fmt.Println(<-result)
}
