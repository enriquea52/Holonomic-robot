#include <stdbool.h>
#include <stdint.h>
// TivaC specific includes
extern "C"
{
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "inc/tm4c123gh6pm.h"
#include "inc/hw_timer.h"

#include "driverlib/timer.h"
#include "driverlib/interrupt.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/pwm.h"
#include "driverlib/pin_map.h"
}
// ROS includes
#include <ros.h>
#include <geometry_msgs/Twist.h>


//Every global variable to be used///////////////////////////////////////////////////////////
int encoder_full = 4320; //4320 ticks para una revolución despues de la reduión de engranes
float sample_time = 0.01 ;
volatile float rpm_conv = 0.0;

volatile int encoder_ticks1= 0;
volatile int encoder_ticks2= 0;
volatile int encoder_ticks3= 0;
volatile int encoder_ticks4= 0;

int test =0;

int real_pos = 0;
int total_ticksh = 0;
int total_ticksv = 0;


//control variables
float dt = 0.0;


float set_rpmv = 0.0; //desired rpm value for vertical motion
float set_rpmh = 0.0; //desired rpm value for horizontal motion

int dirh = 0;
int dirv = 0;

float rpm1= 0.0; //measured rpm from motor 1
float rpm2= 0.0; //measured rpm from motor 2
float rpm3= 0.0; //measured rpm from motor 3
float rpm4= 0.0; //measured rpm from motor 4

float error1 = 0.0;//set_rpmh - rpm1
float error2 = 0.0;//set_rpmv - rpm2
float error3 = 0.0;//set_rpmh - rpm3
float error4 = 0.0;//set_rpmv - rpm4

float past_error1 = 0.0;
float past_error2 = 0.0;
float past_error3 = 0.0;
float past_error4 = 0.0;

float error_sum1 = 0.0;
float error_sum2 = 0.0;
float error_sum3 = 0.0;
float error_sum4 = 0.0;

float kp = 210;
float kd = 0.3;
float ki =  0;



int pwm_signal1 = 0;
int pwm_signal2 = 0;
int pwm_signal3 = 0;
int pwm_signal4 = 0;
///////////////////////////////////////////////////////////



//ROS PUBLISHER
geometry_msgs::Twist twist_msg;
ros::Publisher ticks_count("ticks",&twist_msg);



//Callback for receiving RPM commandds
void callback(const geometry_msgs::Twist& msg)
{
 set_rpmv = msg.linear.y; //desired rpm value for vertical motion
 set_rpmh = msg.linear.x; //desired rpm value for horizontal motion

//Adjusting vertical motor directions
if (msg.angular.y == 0 && msg.angular.z == 0 )
{

 dirv = 0;
 GPIOPinWrite(GPIO_PORTD_BASE,GPIO_PIN_0|GPIO_PIN_6,1); //Salidas de dirección del motor 2     //  64
 GPIOPinWrite(GPIO_PORTE_BASE,GPIO_PIN_0|GPIO_PIN_4,16); //Salidas de dirección del motor 4     // 16
} 
if (msg.angular.y == 1 && msg.angular.z == 0)
{
 dirv = 1;
 GPIOPinWrite(GPIO_PORTD_BASE,GPIO_PIN_0|GPIO_PIN_6,64); //Salidas de dirección del motor 2     //  64
 GPIOPinWrite(GPIO_PORTE_BASE,GPIO_PIN_0|GPIO_PIN_4,1); //Salidas de dirección del motor 4     // 16
} 

//Adjusting horizontal motor directions
if (msg.angular.x == 0 && msg.angular.z == 0)
{
    dirh = 0;
    GPIOPinWrite(GPIO_PORTB_BASE,GPIO_PIN_2|GPIO_PIN_3,4); //Salidas de dirección del motor 3     //  8
    GPIOPinWrite(GPIO_PORTC_BASE,GPIO_PIN_6|GPIO_PIN_7,128); //Salidas de dirección del motor 1    //  128
} 

if (msg.angular.x == 1 && msg.angular.z == 0)
{
    dirh = 1;
    GPIOPinWrite(GPIO_PORTB_BASE,GPIO_PIN_2|GPIO_PIN_3,8); //Salidas de dirección del motor 3     //  8
    GPIOPinWrite(GPIO_PORTC_BASE,GPIO_PIN_6|GPIO_PIN_7,64); //Salidas de dirección del motor 1    //  128
} 

if ( msg.angular.z == 1) //clockwise turn
{   dirv = 10;
    dirh = 10;
    GPIOPinWrite(GPIO_PORTB_BASE,GPIO_PIN_2|GPIO_PIN_3,4); //Salidas de dirección del motor 3     //  8
    GPIOPinWrite(GPIO_PORTC_BASE,GPIO_PIN_6|GPIO_PIN_7,64); //Salidas de dirección del motor 1    //  128
    GPIOPinWrite(GPIO_PORTD_BASE,GPIO_PIN_0|GPIO_PIN_6,1); //Salidas de dirección del motor 2     //  64
    GPIOPinWrite(GPIO_PORTE_BASE,GPIO_PIN_0|GPIO_PIN_4,1); //Salidas de dirección del motor 4     // 16
} 

if ( msg.angular.z == 2) //reverse clockwise turn
{   dirv = 10;
    dirh = 10;
    GPIOPinWrite(GPIO_PORTB_BASE,GPIO_PIN_2|GPIO_PIN_3,8); //Salidas de dirección del motor 3     //  8
    GPIOPinWrite(GPIO_PORTC_BASE,GPIO_PIN_6|GPIO_PIN_7,128); //Salidas de dirección del motor 1    //  128
    GPIOPinWrite(GPIO_PORTD_BASE,GPIO_PIN_0|GPIO_PIN_6,64); //Salidas de dirección del motor 2     //  64
    GPIOPinWrite(GPIO_PORTE_BASE,GPIO_PIN_0|GPIO_PIN_4,16); //Salidas de dirección del motor 4     // 16
} 




}



// ROS nodehandle //and subscriber
ros::NodeHandle nh;
ros::Subscriber<geometry_msgs::Twist> message_sub("RPM",&callback);



extern "C"
{
/////////////MCU GENERAL CONFIGURATIONS FOR SPEED CONTROL OF EACH WHEEL


void PWM_CONFIG(void){

    //Configure PWM Clock to match system
    SysCtlPWMClockSet(SYSCTL_PWMDIV_1);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOC);  //Habilitar los PWMs del puerto C
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOC))
    {}
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);  //Habilitar los PWMs del puerto F
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOF))
    {}

    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);  //The Tiva Launchpad has two modules (0 and 1). Module 1 covers the LED pins
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM1))
    {}
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM0);  //The Tiva Launchpad has two modules (0 and 1). Module 1 covers the LED pins
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM0))
    {}

    GPIOPinConfigure(GPIO_PF2_M1PWM6);
    GPIOPinConfigure(GPIO_PF3_M1PWM7);
    GPIOPinConfigure(GPIO_PC4_M0PWM6);
    GPIOPinConfigure(GPIO_PC5_M0PWM7);

    GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_2|GPIO_PIN_3);
    GPIOPinTypePWM(GPIO_PORTC_BASE, GPIO_PIN_4|GPIO_PIN_5);

    PWMGenConfigure(PWM0_BASE, PWM_GEN_3, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
    PWMGenConfigure(PWM1_BASE, PWM_GEN_3, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);

    PWMGenPeriodSet(PWM0_BASE, PWM_GEN_3, 800);// PWM DE 100 k Hz
    PWMGenPeriodSet(PWM1_BASE, PWM_GEN_3, 800);// PWM DE 100 k Hz


    //PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,200);
    PWMGenEnable(PWM0_BASE, PWM_GEN_3);
    PWMGenEnable(PWM1_BASE, PWM_GEN_3);


    PWMOutputState(PWM1_BASE, PWM_OUT_6_BIT | PWM_OUT_7_BIT, true);
    PWMOutputState(PWM0_BASE, PWM_OUT_6_BIT | PWM_OUT_7_BIT, true);


}


void GPIO(void){ //aqui se trabaja con configurar los GPIO necesarios
    //Habilitar todos los puertos que necesitare

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOC);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);

    GPIOPinTypeGPIOOutput(GPIO_PORTB_BASE,GPIO_PIN_2|GPIO_PIN_3); //Salidas de dirección del motor 3
    GPIOPinTypeGPIOOutput(GPIO_PORTC_BASE,GPIO_PIN_6|GPIO_PIN_7); //Salidas de dirección del motor 1
    GPIOPinTypeGPIOOutput(GPIO_PORTD_BASE,GPIO_PIN_0|GPIO_PIN_6); //Salidas de dirección del motor 2
    GPIOPinTypeGPIOOutput(GPIO_PORTE_BASE,GPIO_PIN_0|GPIO_PIN_4); //Salidas de dirección del motor 4



    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    GPIOPinTypeGPIOInput(GPIO_PORTA_BASE,GPIO_PIN_2|GPIO_PIN_3|GPIO_PIN_4|GPIO_PIN_5); //Entrada para interrupción de encoder
    GPIOPadConfigSet(GPIO_PORTA_BASE,GPIO_PIN_2|GPIO_PIN_3|GPIO_PIN_4|GPIO_PIN_5,GPIO_STRENGTH_2MA,GPIO_PIN_TYPE_STD_WPD); //acondicionar entrada

    }


void CFG_GPIO_INT(void){ //Aqui se confiigura la interrupcion a utlizar

    IntEnable(INT_GPIOA);
    GPIOIntEnable(GPIO_PORTA_BASE,GPIO_PIN_2|GPIO_PIN_3|GPIO_PIN_4|GPIO_PIN_5);
    GPIOIntTypeSet(GPIO_PORTA_BASE,GPIO_PIN_2|GPIO_PIN_3|GPIO_PIN_4|GPIO_PIN_5,GPIO_RISING_EDGE);

    //IntMasterEnable();
}

void Int_GPIOA(void){ //Rutina de interrupcion del encoders
    int StateA;
    StateA=GPIOIntStatus(GPIO_PORTA_BASE,true);
    GPIOIntClear(GPIO_PORTA_BASE,StateA);
    switch(StateA){
    case GPIO_PIN_5:
        encoder_ticks4++;
        break;
    case GPIO_PIN_4:
        encoder_ticks3++;
        break;
    case GPIO_PIN_3:
        encoder_ticks2++;
        break;
    case GPIO_PIN_2:
        encoder_ticks1++;
        break;
    default:
        break;
    }
}



void IntTimer(void){
    TimerIntClear(TIMER0_BASE,TIMER_TIMA_TIMEOUT);




    rpm4=encoder_ticks4*rpm_conv;
    rpm3=encoder_ticks3*rpm_conv;
    rpm2=encoder_ticks2*rpm_conv;
    rpm1=encoder_ticks1*rpm_conv;

    total_ticksv= total_ticksv+((encoder_ticks2+encoder_ticks4)/2.0);
    total_ticksh= total_ticksh+((encoder_ticks1+encoder_ticks3)/2.0);



    real_pos++;
	if (real_pos==50) //se publicara cada 0.5 segundos
	{
	  twist_msg.linear.x = (total_ticksh);
	  twist_msg.linear.y = (total_ticksv);
	  twist_msg.angular.x = dirh;
	  twist_msg.angular.y = dirv;

	  ticks_count.publish(&twist_msg);
	  
	  total_ticksv=0;
	  total_ticksh=0;
	  real_pos=0;
	}  	

  

    encoder_ticks1=0;
    encoder_ticks2=0;
    encoder_ticks3=0;
    encoder_ticks4=0;

    test++;



    //empieza rutina de control
    error1 = set_rpmh - rpm1;
    error2 = set_rpmv - rpm2;
    error3 = set_rpmh - rpm3;
    error4 = set_rpmv - rpm4;


    pwm_signal1 = (kp*error1)+(ki*error_sum1)+(((kd*(error1-past_error1)))/dt);
    past_error1 = error1;
    error_sum1+=(dt*error1);

    pwm_signal2 = (kp*error2)+(ki*error_sum2)+(((kd*(error2-past_error2)))/dt);
    past_error2 = error2;
    error_sum2+=(dt*error2);

    pwm_signal3 = (kp*error3)+(ki*error_sum3)+(((kd*(error3-past_error3)))/dt);
    past_error3 = error3;
    error_sum3+=(dt*error3);

    pwm_signal4 = (kp*error4)+(ki*error_sum4)+(((kd*(error4-past_error4)))/dt);
    past_error4 = error4;
    error_sum4+=(dt*error4);

    /////Motor control 1
    if (pwm_signal1<800 & pwm_signal1>1)
    {
        PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,pwm_signal1);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }
    else if (pwm_signal1>800)
    {   pwm_signal1 =800;
        PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,800);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }
    else if (pwm_signal1<=0)
    {
        pwm_signal1 =1;
        PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,1);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }

    /////Motor control 2
    if (pwm_signal2<800 & pwm_signal2>1)
    {
        PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,pwm_signal2);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }
    else if (pwm_signal2>800)
    {   pwm_signal2 =800;
        PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,800);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }
    else if (pwm_signal2<=0)
    {
        pwm_signal2 =1;
        PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,1);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }

    /////Motor control 3
    if (pwm_signal3<800 & pwm_signal3>1)
    {
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6,pwm_signal3);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }
    else if (pwm_signal3>800)
    {   pwm_signal3 =800;
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6,800);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }
    else if (pwm_signal3<=0)
    {
        pwm_signal3 =1;
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_6,1);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }

    /////Motor control 4
    if (pwm_signal4<800 & pwm_signal4>1)
    {
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7,pwm_signal4);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }
    else if (pwm_signal4>800)
    {   pwm_signal4 =800;
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7,800);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }
    else if (pwm_signal4<=0)
    {
        pwm_signal4 =1;
        PWMPulseWidthSet(PWM0_BASE, PWM_OUT_7,1);
        //PWMSyncUpdate(PWM0_BASE,PWM_GEN_3_BIT);
    }



}




void TIMER(void){
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    TimerConfigure(TIMER0_BASE,TIMER_CFG_PERIODIC);
    TimerLoadSet(TIMER0_BASE,TIMER_A,(SysCtlClockGet()*sample_time)-1);
    TimerEnable(TIMER0_BASE,TIMER_A);

}

void CFG_TIMER_INT(void){
    IntEnable(INT_TIMER0A);
    TimerIntEnable(TIMER0_BASE,TIMER_TIMA_TIMEOUT);
    IntMasterEnable();
}

void Execute(void){
    IntPrioritySet(INT_TIMER0A, 0);
    GPIO(); //se configuran las entradas y salidas digitales
    CFG_GPIO_INT(); //Se configura la interrupcion del encoder
    TIMER(); //aqui se confiugura el timer a utilizar
    CFG_TIMER_INT(); //Aqui se configura la interrupcion del timer
    PWM_CONFIG(); //Configuracion del pwm


}


}



int main(void)
{
  // TivaC application specific code
  MAP_FPUEnable();
  MAP_FPULazyStackingEnable();
  // TivaC system clock configuration. Set to 80MHz.
  //MAP_SysCtlClockSet(SYSCTL_SYSDIV_2_5 | SYSCTL_USE_PLL | SYSCTL_XTAL_16MHZ | SYSCTL_OSC_MAIN);
  SysCtlClockSet(SYSCTL_XTAL_16MHZ|SYSCTL_SYSDIV_2_5|SYSCTL_USE_PLL);


    rpm_conv = 60.0/((float)encoder_full*sample_time);
    dt = sample_time;

    Execute();


  //ROS node configuration
  nh.initNode();
  nh.subscribe(message_sub);//subscribing to topic
  nh.advertise(ticks_count); //publishing to topic


  while (1)
  {

    // Handle all communications and callbacks.
    nh.spinOnce();


  }
}




