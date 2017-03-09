Contest name withheld; Link to self: https://git.io/vy4co

Comments are welcome! P.S. hire me! ;-)

## Algorithm Outline
* determine tree diameter
* hang the tree by the middle of diameter path
* now it's a coloring problem
* extra consideration when diameter comprises odd number of edges

### Determine diameter
Since graph is a tree, diameter can be computed naively as follows:

![option1](https://github.com/dimaqq/competitive-programming/raw/master/subtree-diameter.png "Diameter algorithm")

### Tree colouring

![option1](https://github.com/dimaqq/competitive-programming/raw/master/subtree-even.png "Colouring")

### Odd diameter

When diameter is odd, there are more coloring options. One way to think about this case is the middle edge could be a part of "left" or "right" side.

This algorithm arbitrarily assigns longer branch as the sole left-side branch and the rest on the right side.

![option1](https://github.com/dimaqq/competitive-programming/raw/master/subtree-odd.png "Odd diameter")

Enumerating odd cases presents another problem: wider limits case contains sibling narrower cases.

Ideally enumeration should contain:
* (3,0) - (3,0) strict
* (3,0) - (2,0)
* (3,1) strict - (2,0)
* etc.

Where `(3,0)strict == (3,0) - (2,0)`.

Math can be simplified and strict sets computed only one side:
* (3,0) * (3,0) == (3,0) * [(3,0)strict + (2,0)]
* (3,1)strict * (2,0)
* (2,1) * (2,1) == (2,1) * [(2,0) + (2,1)strict + (1,1)]
* etc.

![option1](https://github.com/dimaqq/competitive-programming/raw/master/subtree-counting-odd.png "Counting odd")
