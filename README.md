# **MinoLab**  
*by Josua Philippot, Félix Yriarte, Bryan Regnauld, Samuel Towndrow-Zebair, Clément Potin*.
#
MinoLab is a small student project simulating a human being chased by a minotor, using python created in early 2021 for our agent programming class.

The aim of this project is to simply simulate two types of agents, a human and a minotor in a randomly generated labyrinth.
They are evolving in a procedurally generated labyrinth, made out of walls, walkable paths, and one or multiples exits.
It is generated by "digging" the paths in the walls, as shown here :
![labyrinth_generation](https://user-images.githubusercontent.com/33656456/132540553-c0a2b5e4-566e-4c1c-b1aa-a3fc8a6cf280.gif)


The walls are represented by "#", the exit(s) by "@" and the walkables areas are left blank.

Each type of agent pursue their own goal :
  - The human(s) tries to escape the labyrinth, using a Depth-First Search, while avoiding the minotor(s).
    A human is represented by "H", a simple human walkthrough would likely look like that :
    ![human_walkthrough](https://user-images.githubusercontent.com/33656456/132533397-99b179df-36de-4dbf-b163-4a16c388dddc.png)
    As previously said, when encoutering a minotor (when it's in its line of sight), the human will try to avoid it. This behavior will typically look like this :
    ![human_avoiding_minotor](https://user-images.githubusercontent.com/33656456/132534880-5c0c22a6-d3db-45ac-b859-39630eaaf89f.png)

  - The minotor(s) randomly wander in the labyrinth, until it stumble upon a human smell, it will then proceed the chase the human(s) until it's able to kill it.
    A minotor is represented by "M", a simple minotor walkthrough would likely look like that :
    ![minotor_walkthrough](https://user-images.githubusercontent.com/33656456/132536185-900a7a9e-8615-4181-9240-d70f760749bc.png)
    Here, just like in the program, the human smell is hidden, if we wanted to visualize it, it would then look like this :
    ![minotor_and_smell](https://user-images.githubusercontent.com/33656456/132540624-15f39a09-8ad4-43ac-9055-23908acafba3.png)

# Disclamer
This program is just a prototype to show our comprehension of agent programming and our ability to apply our knowledge from scratch. As a consequence, it is very likely that you encounter some issues while running it. We do not plan to make it work flawlessly.

Also, the variable names and most of the commentary is written in French, it is due to the fact that, again, it is a student project.

If you find anything that might help you in this program, feel free to use it :)
   
