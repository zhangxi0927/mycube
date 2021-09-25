int i=0;
String answer="";
int f=0;
int x;
int y;
int m;
int n;
int a;
int b;
int flag;
int flagg;

void setup()
{
  Serial.begin(9600);
  pinMode(PA0,OUTPUT); // Step down
  pinMode(PA1,OUTPUT); //  Dir

  pinMode(PA5,OUTPUT); // Step back
  pinMode(PA6,OUTPUT); // Dir

  pinMode(PA7,OUTPUT); // Step right
  pinMode(PB6,OUTPUT); // Dir

  pinMode(PB8,OUTPUT); // Step left
  pinMode(PB9,OUTPUT); // Dir

  pinMode(PC8,OUTPUT); // Step front
  pinMode(PC6,OUTPUT); // Dir

  pinMode(PB14,OUTPUT); // Step up
  pinMode(PB13,OUTPUT); // Dir
}

void loop()
{
  while(Serial.available()>0){
    
    answer+=char(Serial.read());
    Serial.print(answer);
    i++;
    delay(2);
  }
  Serial.print(answer);

  for(int a=0;a<i;a++){
    if(answer[a]=='F'){
//      flag=1;
//      flagg=1;
      if(answer[a+1]=='3'){
//         if(flag){
          digitalWrite(PC6,LOW); // Set Dir high
           for(x = 0; x < 50; x++){
            digitalWrite(PC8,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PC8,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
           }
           //flag=0;
           delay(1000); // pause one second
//         }
      }
      if(answer[a+1]=='2'){
//        if(flagg){
          digitalWrite(PC6,HIGH); // Set Dir high
          for(y = 0; y < 100; y++){
            digitalWrite(PC8,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PC8,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      if(answer[a+1]=='1'){
//        if(flagg){
          digitalWrite(PC6,HIGH); // Set Dir high
          for(y = 0; y < 50; y++){
            digitalWrite(PC8,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PC8,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      flag=1;
      flagg=1;
    }


    if(answer[a]=='B'){
      flag=1;
      flagg=1;
      
      if(answer[a+1]=='3'){
//         if(flag){
          digitalWrite(PA6,LOW); // Set Dir high
           for(x = 0; x < 50; x++){
            digitalWrite(PA5,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PA5,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
           }
//           flag=0;
           delay(1000); // pause one second
//         }
      }
      if(answer[a+1]=='2'){
//        if(fla gg){
          digitalWrite(PA6,HIGH); // Set Dir high
          for(y = 0; y < 100; y++){
            digitalWrite(PA5,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PA5,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      if(answer[a+1]=='1'){
//        if(flagg){
          digitalWrite(PA6,HIGH); // Set Dir high
          for(y = 0; y < 50; y++){
            digitalWrite(PA5,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PA5,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      flag=1;
      flagg=1;
    }


    if(answer[a]=='U'){
      flag=1;
      flagg=1;
      
      if(answer[a+1]=='3'){
//         if(flag){
          digitalWrite(PB13,LOW); // Set Dir high
           for(x = 0; x < 50; x++){
            digitalWrite(PB14,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PB14,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
           }
//           flag=0;
           delay(1000); // pause one second
//         }
      }
      if(answer[a+1]=='2'){
//        if(flagg){
          digitalWrite(PB13,HIGH); // Set Dir high
          for(y = 0; y < 100; y++){
            digitalWrite(PB14,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PB14,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      if(answer[a+1]=='1'){
//        if(flagg){
          digitalWrite(PB13,HIGH); // Set Dir high
          for(y = 0; y < 50; y++){
            digitalWrite(PB14,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PB14,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      flag=1;
      flagg=1;
    }


    if(answer[a]=='D'){
      flag=1;
      flagg=1;
      
      if(answer[a+1]=='3'){
//         if(flag){
          digitalWrite(PA1,LOW); // Set Dir high
           for(x = 0; x < 50; x++){
            digitalWrite(PA0,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PA0,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
           }
//           flag=0;
           delay(1000); // pause one second
//         }
      }
      if(answer[a+1]=='2'){
//        if(flagg){
          digitalWrite(PA1,HIGH); // Set Dir high
          for(y = 0; y < 100; y++){
            digitalWrite(PA0,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PA0,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      if(answer[a+1]=='1'){
//        if(flagg){
          digitalWrite(PA1,HIGH); // Set Dir high
          for(y = 0; y < 50; y++){
            digitalWrite(PA0,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PA0,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      flag=1;
      flagg=1;
    }


    if(answer[a]=='R'){
      flag=1;
      flagg=1;
      
      if(answer[a+1]=='3'){
//         if(flag){
          digitalWrite(PB6,LOW); // Set Dir high
           for(x = 0; x < 50; x++){
            digitalWrite(PA7,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PA7,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
           }
//           flag=0;
           delay(1000); // pause one second
//         }
      }
      if(answer[a+1]=='2'){
//        if(flagg){
          digitalWrite(PB6,HIGH); // Set Dir high
          for(y = 0; y < 100; y++){
            digitalWrite(PA7,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PA7,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      if(answer[a+1]=='1'){
//        if(flagg){
          digitalWrite(PB6,HIGH); // Set Dir high
          for(y = 0; y < 50; y++){
            digitalWrite(PA7,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PA7,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      flag=1;
      flagg=1;
    }



    if(answer[a]=='L'){
      flag=1;
      flagg=1;
      
      if(answer[a+1]=='3'){
//         if(flag){
          digitalWrite(PB9,LOW); // Set Dir high
           for(x = 0; x < 50; x++){
            digitalWrite(PB8,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PB8,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
           }
//           flag=0;
           delay(1000); // pause one second
//         }
      }
      if(answer[a+1]=='2'){
//        if(flagg){
          digitalWrite(PB9,HIGH); // Set Dir high
          for(y = 0; y < 100; y++){
            digitalWrite(PB8,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PB8,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      if(answer[a+1]=='1'){
//        if(flagg){
          digitalWrite(PB9,HIGH); // Set Dir high
          for(y = 0; y < 50; y++){
            digitalWrite(PB8,HIGH); // Output high
            delayMicroseconds(1600); // Wait 1/2 a ms
            digitalWrite(PB8,LOW); // Output low
            delayMicroseconds(1600); // Wait 1/2 a ms
          }
//          flagg=0;
          delay(1000); // pause one second
//        }
      }
      flag=1;
      flagg=1;
    }

  }
  
  answer="";

  flag=0;
  flagg=0;

  
}
