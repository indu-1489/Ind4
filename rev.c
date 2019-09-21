#include<stdio.h>
#include<string.h>
int main()
{
	char str[100],rev[100];
	gets(str);
	int i=0,count=0,j=0;
	while(str[i]!='\0')
	{
		count++;
		i++;
	}
	for(i=count-1;i>=0;i--)
	{
		rev[j]=str[i];
		j++;
	}
	printf("%s",rev);
}
