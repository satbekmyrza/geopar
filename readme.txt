- INTENT:
  This project is an example of Computational Reasoning application, and acts as a geometric theorems
  prover. More specifically, it is designed to prove Morley's Trisector Theorem (as of June 2016).


- FUNCTIONALITY:
  The program operates according to the diagram in "Geopar - UML Diagram" google slides.
  Link to "Geopar - Diagrams":
  https://docs.google.com/presentation/d/1NkYzuc2SvzuM0E-Suw00hTjIOd0kKMthwJZFddhUuCc/edit?usp=sharing


- TO RUN THE PROJECT:
  Execute run.py script.


- FORMAT OF INPUT.TXT:
  input.txt file serves as an input source for the project. It contains data about the vertices
  and the angles of a triangulated figure.

  The number [n] on the first line in input.txt denotes the number of triangles in the triangulated figure.
  The following [n] lines denote the vertices and angles of each triangle in the triangulated figure.
  The program will process first [n+1] lines in input.txt and neglect the remaining part.

  The angles are written as three integer values [a, b, c], each of which is a coefficient
  of an angle of the form [aα + bβ + c], where [α] and [β] are variables.
  The program is able to work with unknown angles. Unknown angles are written with a symbol 'x'.

  This is an example of an information about triangle with all known angles:
  1, 3, 5; -1 -1 60, 0 1 0, 1 0 120
  Vertices: [1, 3, 5]
  Angles: [-α-β+60, β, α+120]
  Please note that vertices and angles correspond to each other via their indices in the list.

  This is an example of an information about triangle with one unknown angle:
  1, 5, 4; -1 -1 60, 0 1 60, x
  Vertices: [1, 5, 4]
  Angles: [-α-β+60, β+60, unknown]

  Note: the program processes only the first triangle configuration in input.txt.
  Thus, you may store all your configurations in input.txt, and move the one of interest to the top
  before running the program.


- EXAMPLE CONFIGURATIONS:
  Preparing an input file may be frustrating at the first time, because any missed detail will lead to
  improper program work. Below are some examples of triangle configurations:
  - Simple triangle that requires pairing (CLASSIC PYRAMID). Link:
    https://drive.google.com/open?id=1FBQ49obyUkgOncR4zO6KU7kQ88qRqlQWlRiMV95feHQ
  - Morley with alphas, betas, and angles in equilateral triangle known (MORLEY INCOMPLETE). Link:
    https://drive.google.com/open?id=172aspdJkZt9o6HyFKOKixCu8vuHe9FLwtaipAVcAuM4


- ISSUES:
  - see triangle.py
  - see angle.py
