import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def pivotphase1(data,original_lpp_length):
    for i in range(0,original_lpp_length):
        quotientcomp=[]
        if data.iloc[-1,i]<0:
            for j in range(0,len(data)-2):
                if data.iloc[j,i]>0:
                    quotientcomp.append(data.iloc[j,-1]/data.iloc[j,i])
                else:
                    quotientcomp.append(float('inf'))
            winner=quotientcomp.index(min(quotientcomp))
            data.iloc[winner,:]=data.iloc[winner,:]/data.iloc[winner,i]
            for j in range(0,len(data)):
                if j!=winner:
                    data.iloc[j,:]=data.iloc[j,:]-data.iloc[j,i]*data.iloc[winner,:]
    for i in range(0,original_lpp_length):
        if data.iloc[-1,i]<0:
            pivotphase1(data,original_lpp_length)
    return data


def pivotphase2(data):
    for i in range(0,len(data.columns)-1):
        quotientcomp=[]
        if data.iloc[-1,i]<0:
            for j in range(0,len(data)-1):
                if data.iloc[j,i]>0:
                    quotientcomp.append(data.iloc[j,-1]/data.iloc[j,i])
                else:
                    quotientcomp.append(float('inf'))
            winner=quotientcomp.index(min(quotientcomp))
            data.iloc[winner,:]=data.iloc[winner,:]/data.iloc[winner,i]
            for j in range(0,len(data)):
                if j!=winner:
                    data.iloc[j,:]=data.iloc[j,:]-data.iloc[j,i]*data.iloc[winner,:]
        if data.iloc[-1,i]<0 and any(item>0 for item in data.iloc[0:-1,i].values.tolist()[0]):
            pivotphase2(data)
        elif data.iloc[-1,i]<0 and all(item<=0 for item in data.iloc[0:-1,i].values.tolist()[0]):
            return 'Phase2: Theorem 2 applies: LPP is Not Bounded Below'
    return data

def SimplexAlg(listoflists):
    checkerlist=[]
    for i in range(0,len(listoflists)-2):
        templist=list(np.repeat(0,len(listoflists)))
        templist[i]=1
        checkerlist.append(templist)
    finalcheckerlist=[]
    for i in range(0,len(checkerlist)):
        finalcheckerlist.append(checkerlist[i][0:-1])
    if all(item in np.array(listoflists).transpose().tolist() for item in checkerlist):
        print('Phase 1: Theorem 1 applies: LPP is feasible')
        print('')
        data=pd.DataFrame(listoflists).rename(columns={len(listoflists[0])-1:'output'})[0:-1]
        finalresult=pivotphase2(data)
        if type(finalresult)!=str:
            solution=[]
            print('Phase 2: Theorem 1 applies: solution is: ',-finalresult.iloc[-1,-1])
            print('')
            for i in range(0,len(finalresult.columns)-1):
                if list(finalresult.iloc[:,i]) in finalcheckerlist:
                    solution.append(finalresult.iloc[list(finalresult.iloc[:,i]).index(1),-1])
                else:
                    solution.append(0)
            print('Attained at', solution)
            return finalresult
        else:
            return finalresult
    else:
        tempframe=pd.DataFrame(listoflists)
        tempframe2=tempframe.iloc[:,0:-1]
        output=list(tempframe.iloc[:,-1])
        
        checkerlist2=pd.DataFrame(checkerlist).T
        checkerlist2=checkerlist2.iloc[0:-1,:]
        checkerlist2=checkerlist2.append(pd.DataFrame(np.repeat(1,len(checkerlist2.iloc[1,:]))).T).reset_index(drop=True)
        checkerlist2=checkerlist2.T.values.tolist()                  
        for i in range(0,len(checkerlist)):
            tempframe2['art'+str(i+1)]=checkerlist2[i]                        
        tempframe2['output']=output
        for i in range(0,len(tempframe2)-2):
            tempframe2.iloc[-1,:]=tempframe2.iloc[-1,:]-tempframe2.iloc[i,:]   
        phase1frame=pivotphase1(tempframe2,len(listoflists[0])-1)  
        if all(item>=0 for item in list(phase1frame.iloc[-1,0:-1])) and phase1frame.iloc[-1,-1]==0:
            print('Phase 1: Theorem 1 applies: LPP is feasible')
            print('')
            finalresult=phase1frame.iloc[:,0:len(listoflists[0])-1]
            finalresult['output']=phase1frame['output']
            finalresult=finalresult[0:-1]
            finalresult=pivotphase2(finalresult)
            if type(finalresult)!=str:
                solution=[]
                print('Phase 2: Theorem 1 applies: solution is: ', -finalresult.iloc[-1,-1])
                print('')
                for i in range(0,len(finalresult.columns)-1):
                    if list(finalresult.iloc[:,i]) in finalcheckerlist:
                        solution.append(finalresult.iloc[list(finalresult.iloc[:,i]).index(1),-1])
                    else:
                        solution.append(0)
                print('Attained at: ',solution)
                return finalresult
            else:
                return finalresult
        else:
            print('Phase 1: infeasible solution')
            finalresult=phase1frame
            return finalresult