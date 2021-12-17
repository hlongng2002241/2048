# 2048 AI
## Introduction
+ A capstone project for Introduction to Artificial Intelligence course.
+ A quick introduction of the problem: you should check file introduction.pdf in docs folder for more information.
+ All classes information are in `docs/Classes.md`, I recommend you to read this file before coding.

## Collaborators
We are K65 of major Data Science and Artificial Intelligence of Hanoi University of Science and Technology.
+ Hoàng Văn An
+ Nguyễn Ngọc Dũng
+ Nguyễn Huy Hải
+ Nguyễn Hải Long
+ Dương Vũ Tuấn Minh

## Guide to GitHub
You should follow the following steps to get yourself familiar with GitHub. Things might get seriously worse if you do something wrong, basically bacause we are coding together. You can see the GitHub's official guide [here](https://guides.github.com/activities/hello-world/) if you cannot do some steps.

+ Step 1: I think it will be the best for you to use GitHub Desktop. Download it and do the following jobs.

You MUST understand, and know how to do the following things using GitHub to manage a project, BEFORE doing anything in this repository (feel free to skip this part if you already know how to use GitHub):

+ Step 2: Create a repository of your own.
+ On that repository...
  + When you start working on the project for the first time:
    + Step 3: `clone`: clone the repository to your local machine.
  + Create, delete, and adjust files (for the first time and later times):
    + Step 4: `fetch` and `pull`: "sync" everything that you and others have done on the repository from cloud to your local machine, you must do this EVERY TIME you start coding.
    + Step 5: Create and write a Python `hello_world.py` file in that directory. I recommend using Visual Studio Code, but you can use any IDE/editor that you are familiar with.
    + Step 6: `commit`: "make a change" to what you have done in the repository, locally. (Each commit could have multiple files change). Please, write a meaningful commit message, in which you shortly describe all what you have done (e.g. create hello_world).
    + Step 7: `push`: "push all changes", i.e. "sync" your recent commit(s) from your local machine to cloud. (Each push could have multiple commits). The best practice is to split your work in an afternoon to multiple tasks, commit each task, and push it right after each commit. (If you cannot push because of files' conflict, do not try to push the conflict up, and let everyone knows about those files right away).
    + Step 8: Take a look at your repository on the web to see your pushed commits. 
  + By now, you have a hands-on experience with basic GitHub, let's practice!
    + Step 9: Repeat from step 4 to step 8, instead in step 5, you can try to create more files, delete some files, adjust some code, and it will work magically the same way you create the `hello_world.py` file.

## Quick view to directories in this project
The directory:
+ `algorithm`: contains files related to algorithm implementation.
+ `docs`: documents files, included the introduction, the preview image of our production and other information
+ `fonts`: contains shared fonts used in many parts of the program
+ `game`: scripts to implement the main game
+ `src`: the controller of entire application, game play, menu and all algorithms stays here
+ `ui`: base implementation for user interface

Run our program from main.py file

## End-to-end rules to work in this project
+ General rules
  1. (GitHub `fetch`) You must `fetch` (and `pull`) every time before making changes and/or uploading to the repo.
  2. (GitHub `commit` message) You should write a meaningful (and short) commit message. Description is helpful if you are making lots of changes.
  3. (GitHub files' conflict) You must announce everyone if you cannot push because of files' conflict.
  4. (To avoid files' conflict) I recommend you to create your own branches to implement your work. Also, all shared files are pushed into `main` branch, usually files related to game play and program interface.
+ Coding rules
  1. (Name conventions): 
      ```
      + for normal variable:          use lower snake case: snake_case.
      + for constant variable:        use upper snake case: SNAKE_CASE.
      + for function:                 same as normal variable.
      + for class:                    use capital camel case: CapitalCamelCase.
      + in class:
         + for public variable:      same as normal variable.
         + for protect variable:     use `_` prefix with lower snake case: _protect_value
         + for private variable:     use `__` prefix with lower snake case: __private_value
      ```
  2. (Comment conventions) You must comment for every object and every method.
      + Comment format for method:
        ```
        def <name_function>(<parameters>) -> <return_type>:
            """
            <method_description>

            Parameters
            ----------
                <parameter_name>: <type>, default = ... (if you have default value)
                    <parameter_description>

            Returns
            -------
                <return_name>: <type>
                    <return_description>
            """
        ```
   
      + example:
        ```python
        def has_no_move(self, board: list=None) -> bool:
            """
            Check if there is any movement can be applied in the given board
          
            Parameters
            ----------
                board: list, default = None
                    4x4 board
                    if board is None grid's board is used
          
            Returns
            -------
                value: bool
            """
        ```

      + comment for object: write in the line above object declaration. 

      + If the names are meaningful, no comment is feasible

  3. (`=` arrangement) for readable code, we should write `=` like this:
      ```python
      self._current_score     = 0
      self._best_score        = 0
      self.titles             = ['SCORE', 'BEST']

      self.font_title         = SharedFont().get_font(self.TITLE_SIZE)
      self.font_title.bold    = True
      ```

      + note: use tab to arrange

  4. (OOP) You must use Object Oriented Programming, and try to avoid writing too much code in the main program without putting them in an object.
  5. (Absolute import) Most of the time, if you want to use an object from another folders, you should use [absolute import](https://www.geeksforgeeks.org/absolute-and-relative-imports-in-python/).
  6. (No Jupyter) Avoid using Jupyter notebook to code, but there will be some for reporting.
