library(tidyverse)
library(leaps)
library(ISLR)
library(MASS)
library(tree)
atpMatchesClean=read_rds('atpMatchesClean.RDS')
#create variable to show if servers faced break point or not 
atpMatchesClean<-atpMatchesClean %>% mutate(winner=ifelse(winner==1,1,0)) %>% 
  mutate(bkFace=ifelse(bkPtFc1==0&bkPtFc2==0,'none','wait')) %>% 
  mutate(bkFace=ifelse(bkPtFc1!=0&bkPtFc2==0,2,bkFace)) %>% 
  mutate(bkFace=ifelse(bkPtFc1==0&bkPtFc2!=0,1,bkFace)) %>% 
  mutate(bkFace=ifelse(bkPtFc1!=0&bkPtFc2!=0,'both',bkFace)) %>% 
  mutate(winner=factor(winner))

#diff
atpMatchesDiff<-atpMatchesClean %>% 
  dplyr::select(winner,contains('diff'),-c(retFstWondiff,retSndWondiff,pointsDiff,bkSaveDiff)) %>% 
  mutate(winner=factor(winner))

#no diff
linDep<-c('match_id','loser','retFstWon','retSndWon','points','bkPtsSave','netPts_won')
atpMatchesNoDiff<-atpMatchesClean %>% 
  dplyr::select(-contains(c('diff',linDep)))

#both diff and no diff
atpMatchesCleanBoth<-atpMatchesClean %>% dplyr::select(-contains(linDep))

set.seed(2019)



#diff
trainIndex<-sample(1:nrow(atpMatchesDiff),trunc(.8*nrow(atpMatchesDiff)))

train=atpMatchesDiff[trainIndex,]
test=atpMatchesDiff[-trainIndex,]
regFit<-regsubsets(winner~.,data=train,method = 'exhaustive',really.big = T,nvmax=12)


bicResults=data.frame(nVar=1:length(summary(regFit)$cp),BIC=summary(regFit)$bic)


bicResults %>%mutate(color = min(BIC) == BIC) %>% 
  ggplot(aes(x=nVar,y=BIC)) +
  geom_line()+
  geom_point(aes(color=color)) +
  scale_x_continuous(breaks=1:12)+
  scale_color_manual(values=c(NA,'red'))+
  theme_light()+
  theme(legend.position = 'none')
coef(regFit,7)
logModel<-train %>% 
  glm(winner~fstSvWonDiff+sndSvWonDiff+dfDiff+winDiff+UEdiff+forcedPointsDiff+unRetDiff,family = 'binomial',data=.)
ldaModel<-train %>% lda(winner~fstSvWonDiff+sndSvWonDiff+dfDiff+winDiff+UEdiff+forcedPointsDiff+unRetDiff,data = .)
qdaModel<-train %>% qda(winner~fstSvWonDiff+sndSvWonDiff+dfDiff+winDiff+UEdiff+forcedPointsDiff+unRetDiff,data = .)

treeModel<-tree(winner~fstSvWonDiff+sndSvWonDiff+dfDiff+winDiff+UEdiff+forcedPointsDiff+unRetDiff,data = train)
plot(treeModel)
text(treeModel,splits = T,digits = 3)

pLog<-round(predict(logModel,test,type='response'))
mean(pLog==test$winner)

pLDA<-predict(ldaModel,test,type='response')$class
mean(pLDA==test$winner)

pTree<-predict(treeModel,test,type='class')
mean(pTree==test$winner)

pQDA<-predict(qdaModel,test,type='response')$class
mean(pQDA==test$winner)

# no diff


trainNoDiff=atpMatchesNoDiff[trainIndex,]
testNoDiff=atpMatchesNoDiff[-trainIndex,]

regFitNoDiff<-regsubsets(winner~.,data=trainNoDiff,method = 'forward',really.big = T,nvmax=30)
summary(regFitNoDiff)$bic

bicResultsNoDiff=data.frame(nVar=1:length(summary(regFitNoDiff)$bic),BIC=summary(regFitNoDiff)$bic)


bicResultsNoDiff %>%mutate(color = min(BIC) == BIC) %>% 
  ggplot(aes(x=nVar,y=BIC)) +
  geom_line()+
  geom_point(aes(color=color)) +
  scale_x_continuous(breaks=1:29)+
  scale_color_manual(values=c(NA,'red'))+
  theme_light()+
  theme(legend.position = 'none')
names(coef(regFitNoDiff,15))
logModel<-train %>% 
  glm(winner~fstSvWonDiff+sndSvWonDiff+dfDiff+winDiff+UEdiff+bkWonDiff+bkPtFcDiff+forcedPointsDiff+unRetDiff,family = 'binomial',data=.)
ldaModel<-train %>% lda(winner~fstSvWonDiff+sndSvWonDiff+dfDiff+winDiff+UEdiff+bkWonDiff+bkPtFcDiff+forcedPointsDiff+unRetDiff,data = .)
qdaModel<-train %>% qda(winner~fstSvWonDiff+sndSvWonDiff+dfDiff+winDiff+UEdiff+bkWonDiff+bkPtFcDiff+forcedPointsDiff+unRetDiff,data = .)

treeModel<-tree(winner~fstSvWonDiff+sndSvWonDiff+dfDiff+winDiff+UEdiff+bkWonDiff+bkPtFcDiff+forcedPointsDiff+unRetDiff,data = train)
plot(treeModel)
text(treeModel,splits = T,digits = 3)

pLog<-round(predict(logModel,test,type='response'))
mean(pLog==test$winner)

pLDA<-predict(ldaModel,test,type='response')$class
mean(pLDA==test$winner)

pTree<-predict(treeModel,test,type='class')
mean(pTree==test$winner)

pQDA<-predict(qdaModel,test,type='response')$class
mean(pQDA==test$winner)
logModel
atpMatchesDiff$dfDiff

# diff and no diff 