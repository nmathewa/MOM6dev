This is documentation of tools used 


# GIT 

## Installation

```
sudo apt-get install git
```




## Clone an repo

![](resources/git_home.png)

```
git clone https://github.com/nmathewa/MOM6dev

```

## Setup

```
git config --global user.name “[firstname lastname]”

git config --global user.email “[valid-email]”
```


## PUSH for Local changes to remote

ACP - Add,Commit,Push

1. Add files to the queue (stage files)
```
git add --all
```

2. Commit the final changes 

```
git commit -m "First changes"
```

3. Push to remote server (git)

```
git push
```


## Cheat-sheet

[Basic GiT commands](resources/git-cheat-sheet-education.pdf)


# TMUX

With Tmux we can easily switch between multiple programs in one terminal, detach them and reattach them to a different terminal

1. Installation
```BASH
sudo apt-get install tmux
sudo yum install tmux
sudo pacman -S tmux
```

2. Create a session 
```BASH 
tmux
```
or

```
tmux new -s mom6
```

3. attach a session

```BASH
tmux ls

tmux attach -t mom6

```

# CONDA

1. Create an new enviornment
```BASH
conda create --name mom6
```
- mom6 is the enviornment name
- [conda cheatsheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)
