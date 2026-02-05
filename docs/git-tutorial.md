# TL;DR

Get the local repository by running
```shell
$ git clone https://github.com/amadeusdotpng/software-engineering-uark.git

# use this if you're using SSH keys
$ git clone git@github.com:amadeusdotpng/software-engineering-uark.git

$ cd software-engineering-uark
```

Don't edit the main branch directly make a feature branch instead!
```shell
# check what branch you're in
$ git branch

# make a new branch
$ git branch <branch-name> # creates a branch
$ git switch <branch-name> # switches to the new branch
```

I'm done adding and/or editing some files!
```shell
# make sure you're in your feature branch first!
$ git switch <feature-branch>
$ git add <files>
$ git status # optional
$ git commit
```

I'm so so ready to push my commits to GitHub!
```shell
git push -u origin <feature-branch> # if it's your first push in this branch
git push                            # if you've already pushed in thsi branch
```

It seems like someone's updated the main branch... I need to make sure I'm using
the latest main branch in my code!
```shell
git switch main
git pull --rebase # get commits from the remote repository

git switch <feature-branch>
git rebase main # use the newest code from the main branch in your feature branch
```

I'm getting conflicts! I'm going to read the "Resolving Conflicts" section
because it's too long for a TL;DR.

I am done implementing my awesome new feature! Let's merge it to the main branch
```shell
# make sure that the code is using the latest main branch
$ git switch main
$ git pull --rebase
$ git switch <feature-branch>
$ git rebase main

# merge to the main branch. --no-ff to make a commit for the merge.
$ git switch main
$ git merge --no-ff <feature-branch>
$ git push
```

Hooray you've just implemented a new feature and merged it to the main branch. I
sure hope it doesn't crash prod!

# Cloning a Repository
Notable commands used in this section: `git clone`

If you haven't installed Git already, install it [here](https://git-scm.com/install).

To get our repository that's on GitHub, run
```shell
$ git clone https://github.com/amadeusdotpng/software-engineering-uark.git
$ cd software-engineering-uark
```

Now you're in your local repo!

# Branching
Notable commands used in this section: `git branch`, `git switch`, `git checkout`.

Once you've cloned the repo, you're probably on the main branch. You can check
by running
```shell
$ git branch
```
This also displays any other branches that's on your local repo.

Before you add or edit some code, we want to create a new branch so that we're
not directly messing with the main branch. To create a new branch, run
``` shell
$ git branch <branch-name> # creates a branch
$ git switch <branch-name> # switches to the new branch

# you can also do this, which creates a new branch and automatically switches to it
$ git checkout -b <branch-name>
```

We are going to create a new branch for each new feature/task that we do. This
is so that it's awesome and organized but also because it helps prevent
conflicts, which we will talk about later.

# Adding and Committing
Notable commands used in this section: `git add`, `git status`, `git commit`, `git log`

Once you're done adding or editing some files, make sure that you're on your
branch and run
```shell
# make sure you're in your feature branch first!
$ git switch <feature-branch>

$ git add <files>

# make sure that you're about to commit all the files you want and you're not committing something you don't want
$ git status

$ git commit
```
This should make your default editor pop up with some stuff. This is where you
will write your commit message. The first line is typically the title that
summarizes what you've done in your commit. Adding two newlines then more text
is usually some extra details.

If you have a short commit message, you can instead run
```shell
$ git commit -m "<your-commit-message>"
```

*I personally do not care that much for good commit messages since this is not
that serious, but please don't make a commit that adds like 67 files and 80000
new lines of code.* If someone wants to see the new changes that you made, it is
hard to take in all of the files and lines you wrote all at once, unless most of
the files aren't really code then maybe it's okay

## Commit History
You can visualize your commit history along with the branches using
```shell
$ git log --all --decorate --oneline --graph
```

You can make your commit history prettier by following [this StackOverflow post](https://stackoverflow.com/questions/1057564/pretty-git-branch-graphs).

Run this to use what I personally use.
```shell
git config --global alias.lg "log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%n' --all"

```
Now you can run `git lg`.

# Pushing Your Commits to GitHub
Notable commands used in this section: `git push`

Once you're ready to send some commit messages to the GitHub, run
```shell
$ git push
```

If this is the first time you're pushing in this branch, then run
```shell
$ git push -u origin <branch-name>
```

## I Can't Push to Github!
If you're having trouble pushing because Git is saying you're not authenticated
or something, you probably have to set up an SSH key for your GitHub account.

I followed this
[guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).
When I had to do this, I only really looked at "Generating a new SSH key and
adding it to the ssh-agent" and "Adding a new SSH key to your GitHub account".

If you do end up using SSH for Git, you might want to clone the repository using
its SSH url instead.
```shell
$ git clone git@github.com:amadeusdotpng/software-engineering-uark.git
```

If you've already cloned it but it's not letting you push even after you've set
up SSH, you might have to change the remote repository url to the SSH url
```shell
$ git remote set-url origin git@github.com:amadeusdotpng/software-engineering-uark.git
```

Ask Brent, the group chat, (or google.com) for help if you're still stuck!

# Updating Your Local Repo
Notable commands used in this section: `git pull`, `git rebase`, `git merge`

Every once in a while, the main branch gets updated. We want to typically use
the latest main branch in our feature branches. To do this, we can do
```shell
# update the main branch; you can also do this in your feature branch if you're
# working on multiple devices
$ git switch main
$ git pull --rebase

# use changes in the main branch in our feature-branch
$ git switch <feature-branch>
$ git rebase main

# you can also merge if you, for some reason, want to have a commit for updating your branch.
$ git swtich <feature-branch>
$ git merge main
```

It's import to check if your local repo needs to be up to date every once in a
while.

Git will probably tell you there are conflicts when you're trying to keep your
feature branch up to date with the main branch! Read ahead to the "Resolving
Conflicts" section if you're getting this.

# Merging to Main
Notable commands used in this section: `git merge`, `git branch`

Once you're done with your done implementing your feature in your branch, it's
time to merge it to the main branch! Try to make sure that your local repo is
up to date with the remote one by following "Updating Your Local Repo" before
trying to merge to main.
```shell
# we use --no-ff to force git to make a new commit that signifies the merge.
$ git switch main
$ git merge --no-ff <feature-branch>
$ git push
```

This should make your favorite text editor pop up to ask you for a commit
message with a default message ready to go. You can use the default message or
change it if you want!

Since your feature branch is using the latest version of the main branch,
hopefully there won't be any conflicts when merging. You should have dealt with
the conflicts when you did `git rebase main` on your feature branch. If you're
getting a conflict, read on to the next section!

After you're done merging, you can delete your feature branch both in your local
and the remote repositories by running
```shell
$ git branch -d <feature-branch>      # delete the local branch
$ git push -d origin <feature-branch> # delete the remote branch
```

Git actually won't let you delete your local branch unless it's been merged. If
you're totally sure you want to delete your local branch without merging, you
can use
```shell
$ git branch -D <feature-branch>
```

## I Merged to Main Before Updating My Local Repository

If you merged your feature branch to main recently then tried to `git push` the
main branch and got a conflict error, you probably didn't update your local repo
before merging. That's okay, you can just do
```shell
$ git switch main
$ git pull --rebase
```
and resolve any conflicts. After you've taken care of those pesky conflicts, try
to `git push` again!

# Resolving Conflicts

If Git is telling you there are conflicts when you're trying to rebase or merge,
it is surprisingly not too difficult to handle!

When doing a `git rebase main` on your feature branch, Git might tell you
something like
```
Auto-merging my-awesome-code.py
CONFLICT (content): Merge conflict in my-awesome-code.py 
error: could not apply 11030b2... new feature
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
hint: Disable this message with "git config advice.mergeConflict false"
```

This is telling you that there is a conflict in the file `my-awesome-code.py`.
If you open that file in your favorite text editor, you might see something like
```
code code code
<<<<<<< HEAD
something from the main branch
=======
something new you added on your feature branch
>>>>>>> <commit-hash> (<commit-title>)
more code after
```
This means that the code from the main branch, the code above the `=======` is
conflicting with the new code on your feature branch, the code below the
`=======`. 

You just need to delete the code that you don't need and the lines that
Git added, i.e. the  
`<<<<<<< HEAD`, `=======`, and `>>>>>>> <commit-hash> (<commit-title>)`.

For example, if you no longer need the code from the main branch, your file
should now look like
```
code code code
something new you added on your feature branch
more code after
```

If you need both the code from the main branch and in your feature branch, your
file should look like
```
code code code
something from the main branch
something new you added on your feature branch
more code after
```

You can now save the file and run
```shell
$ git add <files>       # add all the files you resolved conflicts in
$ git rebase --continue # finishes the rebase
```

The process is similar for `git merge`. 

If you feel like you've messed something up when you're in the middle of a `git
rebase` or `git merge` you can always run `git rebase --abort` or `git merge
--abort` and then ask for help!

Hooray you've resolved conflicts. Don't forget to delete your branches after
you're done merging if you want!

# Other Notable Things I Didn't Mention

## Pull Requests

Pull requests aren't a part of Git itself but is a part of GitHub or other
alternatives. Pull requests are for others to first review and approve your code
before you marge it to a branch.

I didn't want to require doing pull requests for this project because I feel
like we are all so very busy and I do not want to dump more things to do to you.
However, you are absolutely welcome to make a pull request on GitHub if you want
another person to take a look at your code before merging to main.

## `git init`

The command `git init` is used to initialize a new local repository in the
current working directory.

GitHub should then tell you how to connect a local repository to the one you've
made on your GitHub using `git remote add origin <url>`.

# Meow

If you read all of this you're awesome and also you're basically a god at git
now.
