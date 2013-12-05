hothands <- as.vector(read.table("Dropbox/workspace/poker/hothands.csv", header=FALSE))

zeros <- sum(hothands==0)
ones <- sum(hothands==1)
twos <- sum(hothands==2)
threes <- sum(hothands==3)
fours <- sum(hothands==4)
fives <- sum(hothands==5)
sixes <- sum(hothands==6)

slices <- c(zeros, ones, twos)#, threes, fours, fives, sixes)
slices.all <- c(zeros, ones, twos, threes, fours, fives, sixes)
print(slices.all/10000)

lbls <- c("Zero", "One", "Two")#, "Three", "Four", "Five", "Six")
pie(slices, labels = lbls, main="Hot Hands per Session", col=rainbow(length(lbls)))