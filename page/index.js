async function getInfo(){
            for(let i = 1;i <= 6;i++){
                for(let j = 1;j<= 12;j+=2){
                   let cur = "#"+"b"+i+'-'+j
                   const target = document.querySelector(cur);
                   const res = await eel.test1(i,j)();
                   target.innerHTML = `` + res;
                }
            }
        }
getInfo();
