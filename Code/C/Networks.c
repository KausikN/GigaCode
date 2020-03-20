/*
Summary
Library of Networking C Functions made by ME
*/

// Imports
#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<string.h>
#include<unistd.h>
#include <arpa/inet.h>
#include<time.h>

// General Functions
void NewClient()
{
	char ipaddr[16];
	//printf("Enter IP Address to connect: ");
	//scanf("%s", ipaddr);
	//printf("%s", ipaddr);

	int c_socket;

	char buf[100] = "\nHello server from 123.\n";
	//buf = msg;

	c_socket = socket(AF_INET, SOCK_STREAM, 0);
	struct sockaddr_in client;
	memset(&client, 0, sizeof(client));
	client.sin_family = AF_INET;
	client.sin_port = htons(9009);
	client.sin_addr.s_addr = inet_addr("172.17.4.235");
	if(connect(c_socket, (struct sockaddr *)&client, sizeof(client)) == -1)
	{
		printf("Connection Issue.\n");
		return 0;
	}
	printf("Enter message to transfer: \n");

	//while(1)
	//{
		char msg[100];
		gets(msg);
		strcpy(buf, msg);
		send(c_socket, buf, sizeof(buf), 0);
		recv(c_socket, buf, sizeof(buf), 0);

		printf("Message from Server: %s\n", buf);
	//}

	close(c_socket);
}

void NewServer()
{
	int s_socket, s_server;
	char buf[100] = "hello client";
	s_socket = socket(AF_INET, SOCK_STREAM, 0);

	struct sockaddr_in server, other;
	memset(&server, 0, sizeof(server));
	memset(&other, 0, sizeof(other));

	server.sin_family = AF_INET;
	server.sin_port = htons(9009);
	server.sin_addr.s_addr = INADDR_ANY;

	
	if(bind(s_socket, (struct sockaddr*)&server, sizeof(server)) != -1)
	{
		printf("\nNo errors in bind.\n");
		listen(s_socket, 5);
		socklen_t add;
		add = sizeof(other);
		s_server = accept(s_socket, (struct sockaddr*)&other, &add);
		send(s_server, buf, sizeof(buf), 0);
		recv(s_server, buf, sizeof(buf), 0);
		printf("msg from client: %s", buf);
		close(s_server);
		close(s_socket);
		//while(1);
		return 0;
	}

	printf("\nError in Bind.\n");

	close(s_server);
	close(s_socket);
	
	return 0;
}

int ServerCreate(int port)		// Return 1 for error
{
	s_socket = socket(AF_INET, SOCK_STREAM, 0);

	struct sockaddr_in server, other;
	memset(&server, 0, sizeof(server));
	memset(&other, 0, sizeof(other));

	server.sin_family = AF_INET;
	server.sin_port = htons(port);
	server.sin_addr.s_addr = INADDR_ANY;


	if(bind(s_socket, (struct sockaddr*)&server, sizeof(server)) != -1)
	{
		printf("Server Running.....\n");
		listen(s_socket, 5);

		return 0;

		//int accepterror = AcceptNewClient();
		//return accepterror;
	}
	else
	{
		//printf("\nError in Bind.\n");
		return 1;
	}
}

void * AcceptNewClient(void * p)
{
	//struct sockaddr_in other;
	memset(&other, 0, sizeof(other));
	socklen_t add = sizeof(other);

	s_server = accept(s_socket, (struct sockaddr*)&other, &add);
	if(s_server == -1) ;//return 1;
	else
	{
		printf("\n[+] Conection accepted from %s,%d\n",inet_ntoa(other.sin_addr),ntohs(other.sin_port));
		//return 0;
	}

	pthread_exit(0);
}

int ClientCreate(int port, char IPADDR[])		// Return 1 for error
{
	c_socket = socket(AF_INET, SOCK_STREAM, 0);
	struct sockaddr_in client;
	memset(&client, 0, sizeof(client));
	client.sin_family = AF_INET;
	client.sin_port = htons(port);
	client.sin_addr.s_addr = inet_addr(IPADDR);
	//client.sin_addr.s_addr = INADDR_ANY;
	if(connect(c_socket, (struct sockaddr *)&client, sizeof(client)) == -1)
	{
		printf("Connection Issue.\n");
		return 1;
	}
	else return 0;
}

// CRC Checker
int CRC_Check(char bitarr_crc[], char divisor[], int bitarr_crc_size, int divisor_size)
{
	char x[divisor_size];
	for(int i=0;i<divisor_size;i++) x[i] = bitarr_crc[i];
	x[divisor_size] = '\0';

	

	for(int i=0; i < bitarr_crc_size-divisor_size+1; i++)
	{
		//printf("\nXIN: %s\n", x);

		if(x[0] == '1')
		{
			for(int j=1;j<divisor_size;j++)
			{
				if(x[j] == divisor[j])
				{
					x[j-1] = '0';
				}
				else 
				{
					x[j-1] = '1';
				}
				//printf("\ninterx %d: %c - %c\n", j, divisor[j], x[j]);
			}
		}
		else 
		{
			for(int j=1;j<divisor_size;j++)
			{
				if(x[j] == '0')
				{
					x[j-1] = '0';
				}
				else 
				{
					x[j-1] = '1';
				}
				//printf("\ninterx %d: %s - %c\n", j, "Zero", x[j]);
			}
		}
		
		if(i<bitarr_crc_size-divisor_size+1-1)
		{
			x[divisor_size-1] = bitarr_crc[i+divisor_size];
			//printf("\nFinalBit %d: %c\n", i+divisor_size, bitarr_crc[i+divisor_size]);
		}

		//printf("\nXOUT: %s\n", x);
	}

	int check = 0;
	for(int i=0;i<divisor_size-1;i++)
	{
		if(x[i] != '0') return 1;
	}
	
	return 0;
}

void CRC_Receiver()
{
	printf("----------------------CRC TCP/IP Receiver-----------------------------\n");

	int error = ServerCreate(9009);
	if(error == 1)
	{
		close(s_server);
		close(s_socket);
		printf("Server Binding Issue.\n");
		return 0;
	}
	else 
	{
		printf("\nServer Waiting...\n");

		char bitarr_crc[100];
		char divisor[100];

		int bitarr_crc_size = 0;
		int divisor_size = 0;

		//while(1)
		{
			recv(s_server, divisor, sizeof(divisor), 0);
			recv(s_server, bitarr_crc, sizeof(bitarr_crc), 0);

			bitarr_crc[0] = '1';

			bitarr_crc_size = strlen(bitarr_crc);
			divisor_size = strlen(divisor);

			strcat(bitarr_crc, "\0");
			strcat(divisor, "\0");

			char b[bitarr_crc_size-divisor_size+1];
			char crc[divisor_size-1];
			for(int i=0;i<bitarr_crc_size;i++)
			{
				if(i < bitarr_crc_size-divisor_size+1) b[i] = bitarr_crc[i];
				else crc[i-(bitarr_crc_size-divisor_size+1)] = bitarr_crc[i];
			}

			crc[divisor_size] = '\0';
			b[bitarr_crc_size-divisor_size+1] = '\0';

			int check = CRC_Check(bitarr_crc, divisor, bitarr_crc_size, divisor_size);

			if(check == 0)
			{
				printf("No errors in bit array.\n");
				printf("Received bit array: %s\n", b);
				printf("CRC: %s\n", crc);
			}
			else 
			{
				printf("Bit array has ERROR.\n");
				printf("Received bit array: %s\n", b);
				printf("CRC: %s\n", crc);
			}
		}

		

	}

	close(s_server);
	close(s_socket);

	printf("\n---------------------------------------------------------------------\n");	
	return 0;
}

void CRC_Generate(char bitarr[], char divisor[], int bitarr_size, int divisor_size)
{
    char crc[100];

	char b[100];
	strcpy(b, bitarr);

	for(int i=0;i<divisor_size-1;i++) strcat(b, "0");

	char x[divisor_size];
	for(int i=0;i<divisor_size;i++) x[i] = b[i];
	x[divisor_size] = '\0';

	

	for(int i=0; i < bitarr_size; i++)
	{
		//printf("\nXIN: %s\n", x);

		if(x[0] == '1')
		{
			for(int j=1;j<divisor_size;j++)
			{
				if(x[j] == divisor[j])
				{
					x[j-1] = '0';
				}
				else 
				{
					x[j-1] = '1';
				}
				//printf("\ninterx %d: %c - %c\n", j, divisor[j], x[j]);
			}
		}
		else 
		{
			for(int j=1;j<divisor_size;j++)
			{
				if(x[j] == '0')
				{
					x[j-1] = '0';
				}
				else 
				{
					x[j-1] = '1';
				}
				//printf("\ninterx %d: %s - %c\n", j, "Zero", x[j]);
			}
		}
		
		if(i<bitarr_size-1)
		{
			x[divisor_size-1] = b[i+divisor_size];
			//printf("\nFinalBit %d: %c\n", i+divisor_size, b[i+divisor_size]);
		}

		//printf("\nXOUT: %s\n", x);
	}

	for(int i=0;i<divisor_size-1;i++)
	{
		crc[i] = x[i];
	}
}

void CRC_Transmitter()
{
	printf("----------------------CRC TCP/IP Transmitter-----------------------------\n");

	int error = ClientCreate(9009, 1, "");
	if(error == 1)
	{
		close(c_socket);
		printf("Connection Issue.\n");
		return 0;
	}
	else 
	{
		char bitarr[100];
		char divisor[100];

		int bitarr_size = 0;
		int divisor_size = 0;

		printf("Enter bit array: ");
		scanf("%s", bitarr);

		printf("Enter divisor: ");
		scanf("%s", divisor);

		bitarr_size = strlen(bitarr);
		divisor_size = strlen(divisor);

		printf("\nSizes: bit: %d, div: %d\n", bitarr_size, divisor_size);

		CRC_Generate(bitarr, divisor, bitarr_size, divisor_size);

		printf("Original bit array: %s\n", bitarr);
		printf("CRC: %s\n", crc);

		strcat(bitarr, crc);

		strcat(bitarr, "\0");
		strcat(divisor, "\0");

		send(c_socket, divisor, sizeof(divisor), 0);
		send(c_socket, bitarr, sizeof(bitarr), 0);
		printf("Bit Array Sent.\n");
	}

	close(c_socket);

	printf("\n---------------------------------------------------------------------\n");	
}

// File Transfer
void FileTransfer_Receiver()
{
	printf("----------------------File Transfer TCP/IP Receiver-----------------------------\n");

	int error = ServerCreate(9009);
	if(error == 1)
	{
		close(s_server);
		close(s_socket);
		printf("Server Binding Issue.\n");
		return 0;
	}
	else 
	{
		printf("\nServer Started...\n");

		char filename[100];
		char filename_withext[100] = "";
		char ext[10];

		char buffer[2000];
		char charbuf[1];

		recv(s_server, filename, sizeof(filename), 0);
		recv(s_server, ext, sizeof(ext), 0);

		if(strlen(ext) == 0) return 0;

		strcat(filename_withext, filename);
		strcat(filename_withext, "_recv.");
		strcat(filename_withext, ext);
		
		FILE *fp;
		fp = fopen(filename_withext, "w");

		char endoffile[1] = "0";

		int check = 0;
		while(check == 0)
		{
			/*
			recv(s_server, buffer, sizeof(buffer), 0);

			//printf("buf: %s\n", buffer);

			if(!strcmp(buffer, "end")) check = 1;
			else fprintf(fp, "%s ", buffer);
			*/

			recv(s_server, endoffile, sizeof(endoffile), 0);
			if(endoffile[0] == '1') check = 1;
			else 
			{
				recv(s_server, charbuf, sizeof(charbuf), 0);
				//printf("buf: %s\n", charbuf);
				fprintf(fp, "%c", charbuf[0]);
			}

			//printf("buf: %s\n", charbuf);
			//if(charbuf[0] == '\b') check = 1;
			//else fprintf(fp, "%c", charbuf[0]);

		}
		printf("\n\n File Ended \n\n");

		fclose(fp);
		
		printf("File %s Received Succesfully.\n", filename_withext);
	}

	close(s_server);
	close(s_socket);

	printf("\n---------------------------------------------------------------------\n");	
}

void FileTransfer_Transmitter()
{
	printf("----------------------File Transfer TCP/IP Transmitter-----------------------------\n");

	int error = ClientCreate(9009, 1, "");
	if(error == 1)
	{
		close(c_socket);
		printf("Connection Issue.\n");
	}
	else 
	{
		char filename[100];
		char filename_withext[100];
		char ext[10];

		char buffer[2000];
		char charbuf[1];

		printf("Enter filename: ");
		scanf("%s", filename);

		printf("Enter extension: ");
		scanf("%s", ext);

		strcpy(filename_withext, filename);
		strcat(filename_withext, ".");
		strcat(filename_withext, ext);

		printf("Filename %s.\n", filename_withext);

		FILE *fp;
		fp = fopen(filename_withext, "r");

		printf("File %s opened.\n", filename_withext);

		char endoffile[1] = "0";

		send(c_socket, filename, sizeof(filename), 0);
		send(c_socket, ext, sizeof(ext), 0);

		while(!feof(fp))
		{ 
			/*
			fscanf(fp, "%s", buffer);

			//printf("buf: %s\n", buffer);

			send(c_socket, buffer, sizeof(buffer), 0);
			*/

			fscanf(fp, "%c", &charbuf[0]);
			//printf("buf: %s\n", charbuf);
			send(c_socket, endoffile, sizeof(endoffile), 0);
			send(c_socket, charbuf, sizeof(charbuf), 0);

		}
		/*
		strcpy(buffer, "end");
		send(c_socket, buffer, sizeof(buffer), 0);
		*/
		/*
		charbuf[0] = '\b';
		send(c_socket, charbuf, sizeof(charbuf), 0);
		*/
		printf("\n\n File Ended \n\n");
		endoffile[0] = '1';
		send(c_socket, endoffile, sizeof(endoffile), 0);
		
		printf("buffer Sent.\n");
	}

	close(c_socket);

	printf("\n---------------------------------------------------------------------\n");	
}

// Huffman Encoding
struct lookup{
	char s;
	char code[200];
};

struct lookup LookUpTable[200];

void Huffman_Decoder(char seq[], char chars[], int n){

	char code[200];
	int code_size = 0;

	printf("Decoded sequence: ");
	for(int i=0;i<n;i++)
	{
		code[code_size] = seq[i];
		code_size++;

		char s;

		int flag = 0;
		for(int j=0;j<strlen(chars);j++)
		{
			if(strlen(LookUpTable[(int)chars[j]].code) == code_size)
			{
				int flag2 = 1;
				for(int k=0;k<code_size;k++)
				{
					if(LookUpTable[(int)chars[j]].code[k] != code[k]) flag2 = 0;
				}
				if(flag2 == 1)
				{
					flag = 1;
					s = chars[j];
				}
			}
		}
		if(flag == 1)
		{
			printf("%c", s);
			code_size = 0;
		}
	}
	printf("\n");
}

void HuffmanEncoding_Receiver()
{
	printf("----------------------Huffman Encoding Receiver-----------------------------\n");

	int error = ServerCreate(9009);
	if(error == 1)
	{
		close(s_server);
		close(s_socket);
		printf("Server Binding Issue.\n");
	}
	else 
	{
		printf("\nServer Started...\n");

		char encodedseq[200];
		char chars[200];

		char s[1];
		char code[100];

		recv(s_server, chars, sizeof(chars), 0);
		
		for(int i=0;i<strlen(chars);i++)
		{
			recv(s_server, s, sizeof(s), 0);
			recv(s_server, code, sizeof(code), 0);

			LookUpTable[(int)chars[i]].s = s[0];
			strcpy(LookUpTable[(int)chars[i]].code, code);
		}

		recv(s_server, encodedseq, sizeof(encodedseq), 0);

		printf("\nChars: %s\n\n", chars);
		for(int i=0;i<strlen(chars);i++)
		{
			printf("%c - %s\n", LookUpTable[(int)chars[i]].s, LookUpTable[(int)chars[i]].code);
		}

		Decoder(encodedseq, chars, strlen(encodedseq));
		
		printf("Success.\n");
	}

	close(s_server);
	close(s_socket);

	printf("\n---------------------------------------------------------------------\n");	
}

struct node *rptr=NULL;

struct node{
	struct node *lcptr;
	char sym;
	int freq;
	struct node *rcptr;
};

struct lookup{
	char s;
	char code[200];
};



char s[200];
char ds[200];
int f[200];
int n;
int nc;
struct lookup LookUpTable[200];
int lookup_size;

char encodedseq[200] = "";


////////////////////////////////////////////////////

void ISort(){
	for(int i=1;i<nc;i++){
		for(int j=i;j>0;j--){
			if(f[j-1]>f[j]){
				int temp=f[j];
				f[j]=f[j-1];
				f[j-1]=temp;
				
				char temp2=ds[j];
				ds[j]=ds[j-1];
				ds[j-1]=temp2;
			}
			else break;
		}
	}
}

////////////////////////////////////////////////////

void Read(){
	printf("Enter the string: ");
	scanf(" %[^\n]", s);
	n = strlen(s);
	lookup_size = 0;
}

void count(){
	nc=0;
	for(int i=0;i<n;i++){
		int flag=0;
		//ds[0]=0;
		for(int j=0;j<nc;j++){
			if(s[i]==ds[j]){
				flag=1;
				break;
			}
		}
		if(flag==0 ){
			ds[nc]=s[i];
			nc++;
		}
	}
	for(int i=0;i<nc;i++){
		int cou=0;
		for(int j=0;j<n;j++){
			if(ds[i]==s[j]){
				cou++;
			}
		}
		f[i]=cou;
	}
	
	ISort();

}

void BuildTree(int a[], char c[], int size, struct node *ptrarr[]){
	if(size>1){
		int b[200];
		char t[200];
		struct node *nparr[200];
		struct node *ptr = malloc(sizeof(struct node));
		
		
		int temp=a[0]+a[1];
		int tempi=0;
		
		for(int i=2;i<size;i++){
			if(temp>=a[i]){
				tempi=i-1;
			}
		}
		//printf("\n\ntempi - %d -- temp - %d\n\nSize - %d\n\n", tempi, temp, size);
		int ct=2;
		for(int i=0;i<tempi;i++){
			b[i]=a[ct];
			t[i]=c[ct];
			nparr[i]=ptrarr[ct];
			ct++;
		}
		b[tempi]=temp;
		nparr[tempi]=ptr;
		t[tempi]=0;
		for(int i=tempi+1;i<nc-1;i++){
			b[i]=a[ct];
			t[i]=c[ct];
			nparr[i]=ptrarr[ct];
			ct++;
		}
		
		struct node *lfptr = malloc(sizeof(struct node));
		struct node *rgptr = malloc(sizeof(struct node));
		
		lfptr->sym=c[0];
		lfptr->freq = a[0];
		
		if(ptrarr[0]!=NULL){
			lfptr = ptrarr[0];
		}
		
		rgptr->sym=c[1];
		rgptr->freq = a[1];
		
		if(ptrarr[1]!=NULL){
			rgptr = ptrarr[1];
		}
		
		ptr->sym=0;
		ptr->freq=temp;
		ptr->lcptr=lfptr;
		ptr->rcptr=rgptr;
		rptr=ptr;

		BuildTree(b,t,size-1,nparr);
	}
}

void LookupTable(struct node *ptr, char en[], int ensize, int choice, char chars[]){
	if(choice == 1)
	{
		if(ptr!=NULL)
		{
			if(ptr->lcptr==NULL && ptr->rcptr==NULL)
			{
				lookup_size++;
				int index = (int)(ptr->sym);
				LookUpTable[index].s = ptr->sym;
				for(int i=0;i<ensize;i++)LookUpTable[index].code[i] = en[i];
			}
			else 
			{
				ensize++;
				en[ensize-1] = '0';
				LookupTable(ptr->lcptr, en, ensize, 1, "");
				
				en[ensize-1] = '1';
				LookupTable(ptr->rcptr, en, ensize, 1, "");
			}
		}
	}
	else if(choice == 0)
	{
		int maxnoofbits = 10;

		int noofchars = strlen(chars);

		int noofbits = 1;
		int twopow = 2;
		for(int i=0;i<maxnoofbits;i++)		///////////////////	// MAX NO OF BITS ALLOWED = 10 // ////////////////////////
		{
			if(noofchars <= twopow)
			{
				i = maxnoofbits;
			}
			else
			{
				twopow *= 2;
				noofbits++;
			}
		}

		char code[noofbits];
		for(int i=0;i<noofbits;i++) code[i] = '0';

		for(int i=0;i<noofchars;i++)
		{
			for(int j=0;j<noofbits;j++)
			{
				if(code[j] == '1') code[j] = '0';
				else if(code[j] == '0')
				{
					code[j] = '1';
					j = noofbits;
				}
			}
			LookUpTable[(int)chars[i]].s = chars[i];
			strcpy(LookUpTable[(int)chars[i]].code, code);
			printf("Code: %c - %s\n", chars[i], LookUpTable[(int)chars[i]].code);
		}
	}
	
}

void Huffman_Encoder(){
	printf("Encoded Sequence: ");
	char temp[400];

	for(int i=0;i<n;i++){
		int index = (int)(s[i]);

		printf("%s", LookUpTable[index].code);
		strcat(encodedseq, LookUpTable[index].code);
	}
	printf("\n");
}

void Decoder(char seq[], int nd){
	int cn=0;
	printf("Decoded sequence: ");
	while(cn<nd){
		struct node *ptr = rptr;
		while(ptr!=NULL){
			if(ptr->lcptr==NULL && ptr->rcptr==NULL){
				printf("%c", ptr->sym);
				ptr=NULL;
			}
			else {
				if(seq[cn]=='0')ptr=ptr->lcptr;
				else if(seq[cn]=='1')ptr=ptr->rcptr;
				cn++;
			}
			
		}
	}
	printf("\n");
}

void print(struct node *ptr){
	if(ptr!=NULL){
		print(ptr->lcptr);
		printf("\n");
		printf("%c - %d", ptr->sym, ptr->freq);
		printf("\n");
		print(ptr->rcptr);
	}
}

void HuffmanEncoding_Transmitter()
{
	printf("----------------------Huffman Encoding Transmitter-----------------------------\n");

	rptr=NULL;

	int error = ClientCreate(9009, 1, "");
	if(error == 1)
	{
		close(c_socket);
		printf("Connection Issue.\n");
	}
	else 
	{
		int choice = 0;
		printf("Enter choice of Huffman Encoding(0-const, 1-var): ");
		scanf("%d", &choice);

		Read();
		count();

		printf("\nCharecters: %s\n", ds);
		for(int i=0;i<nc;i++){
			printf("char %c - freq %d\n", ds[i], f[i]);
		}

		if(choice == 1)
		{
			struct node *ptrarr[200];
			for(int i=0;i<nc;i++)ptrarr[i]=NULL;
			BuildTree(f,ds,nc,ptrarr);
			printf("\n\n");
			//print(rptr);

			printf("\n------------Encoder Variable Size----------\n");
			char en[200];
			LookupTable(rptr, en, 0, 1, "");
			Encoder();
			printf("\n----------------------------\n");
		}
		else if(choice == 0)
		{
			printf("\n------------Encoder Constant Size----------\n");
			char en[200];
			LookupTable(rptr, en, 0, 0, ds);
			Encoder();
			printf("\n----------------------------\n");
		}
		



		char s[1];
		char code[100];

		send(c_socket, ds, sizeof(ds), 0);

		for(int i=0;i<strlen(ds);i++)
		{
			s[0] = LookUpTable[(int)ds[i]].s;
			strcpy(code, LookUpTable[(int)ds[i]].code);

			send(c_socket, s, sizeof(s), 0);
			send(c_socket, code, sizeof(code), 0);
		}
		
		send(c_socket, encodedseq, sizeof(encodedseq), 0);
		printf("Sent.\n");
	}

	close(c_socket);

	printf("\n---------------------------------------------------------------------\n");	
}

// Hamming Code
int HammingCode_Check(char arr[], int arr_size)
{
	int errorcheck[arr_size+1];
	for(int i=1;i<=arr_size;i++) errorcheck[i] = -1;

	int pow2 = 1;
	while(pow2 <= arr_size)
	{
		char parity = '0';
		for(int i=pow2;i<=arr_size;i+=pow2*2)
		{
			int j = 0;
			while(j < pow2)
			{
				if(parity == arr[i+j] || i+j == pow2) parity = '0';
				else parity = '1';
				j++;
			}
		}
		if(arr[pow2] == parity)
		{
			for(int i=pow2;i<=arr_size;i+=pow2*2)
			{
				int j = 0;
				while(j < pow2)
				{
					errorcheck[i+j] = 0;
					j++;
				}
			}
		}
		else 
		{
			for(int i=pow2;i<=arr_size;i+=pow2*2)
			{
				int j = 0;
				while(j < pow2)
				{
					if(errorcheck[i+j] == -1) errorcheck[i+j] = 1;
					j++;
				}
			}
		}

		pow2 = pow2 * 2;
	}

	int errno = 0;
	int errindex = -1;

	printf("\nErrors: ");

	int p2 = 1;
	for(int i=1;i<=arr_size;i++)
	{
		printf("%d(%c) ", errorcheck[i], arr[i]);
		if(i == p2)
		{
			p2 = p2 * 2;
		}
		else if(errorcheck[i] == 1)
		{
			errno++;
			errindex = i;
		}
	}
	printf("\n");
	
	if(errno > 1)
	{
		return -2;
	}
	else if(errno == 0) return -1;
	else return errindex;
}

void HammingCode_Receiver()
{
	printf("----------------------HC TCP/IP Receiver-----------------------------\n");

	char arr[100];
	int arr_size = 0;

	printf("Do you want custom array: ");
	int customarrcheck = 0;
	scanf("%d", &customarrcheck);
	if(customarrcheck != 0)
	{
		char temparr[100];

		printf("Enter the array: ");
		scanf("%s", temparr);
		arr_size = strlen(temparr);

		//printf("ArrSA: %s\n", temparr);

		for(int i=1;i<=arr_size;i++)
		{
			arr[i] = temparr[i-1];
		}
		arr[0] = 'B';

		//printf("Arr/0A: %s\n", temparr);

		arr[arr_size+1] = '\0';

		//printf("Arr/0B: %s\n", arr);

		int mid = arr_size/2+1;
		for(int i=1;i<mid;i++)
		{
			char tc = arr[i];
			arr[i] = arr[arr_size-i+1];
			arr[arr_size-i+1] = tc;
		}

		printf("\nReceived message(%d): %s\n", arr_size, arr);

		int check = HammingCode_Check(arr, arr_size);
		if(check == -1) printf("\nNo errors in received message.\n");
		else if(check == -2) printf("\nThere is more than 1 bit error.\n");
		else
		{
			char err = arr[check];
			char corr = 'E';
			if(err == '0') corr = '1';
			else if(err == '1') corr = '0';

			arr[check] = corr;

			printf("There is error in bit %d.\n", check);
			printf("Correction: %c -> %c\n", err, corr);
			printf("Correct array: %s\n", arr);
		}

		printf("\n---------------------------------------------------------------------\n");	
	}

	int error = ServerCreate(9009);
	if(error == 1)
	{
		close(s_server);
		close(s_socket);
		printf("Server Binding Issue.\n");
	}
	else 
	{
		printf("\nServer Waiting...\n");

		while(1)
		{
			recv(s_server, arr, sizeof(arr), 0);

			if(strcmp(arr, "sent") != 0)
			{
				arr_size = strlen(arr);

				printf("\nReceived message(%d): %s\n", arr_size, arr);

				int check = HammingCode_Check(arr, arr_size);
				if(check == -1) printf("\nNo errors in received message.\n");
				else if(check == -2) printf("\nThere is more than 1 bit error.\n");
				else
				{
					char err = arr[check];
					char corr = 'E';
					if(err == '0') corr = '1';
					else if(err == '1') corr = '0';

					arr[check] = corr;

					printf("There is error in bit %d.\n", check);
					printf("Correction: %c -> %c\n", err, corr);
					printf("Correct array: %s\n", arr);
				}
			}
		}
	}

	close(s_server);
	close(s_socket);

	printf("\n---------------------------------------------------------------------\n");	
}

void ReverseArr()
{
	int mid = arr_size/2+1;
	for(int i=1;i<mid;i++)
	{
		arr[i] = arr[arr_size-i];
	}
}

void HammingCode_printArr()
{
	printf("The HC array(%d): ", arr_size);
	for(int i=0;i<arr_size;i++)
	{
		printf("%c ", arr[arr_size-i]);
	}
	printf("\n");
}

void HammingCode_InitArr(char bitarr[], int bitarr_size)
{
	arr[0] = 'B';
	arr_size = 0;

	int pow2 = 2;
	arr[1] = 'R';
	int index = 2;
	for(int i=0;i<bitarr_size;i++)
	{
		if(index == pow2)
		{
			arr[index] = 'R';
			index++;
			pow2 = pow2 * 2;
		}
		arr[index] = bitarr[bitarr_size-i-1];
		index++;
	}

	arr_size = index-1;
}

void HammingCode_Generate(char bitarr[], int bitarr_size)
{
	HammingCode_InitArr(bitarr, bitarr_size);

	printf("\nBefore Red,\n");
	HammingCode_printArr();


	int pow2 = 1;
	while(pow2 <= arr_size)
	{
		char parity = '0';
		for(int i=pow2;i<=arr_size;i+=pow2*2)
		{
			int j = 0;
			while(j < pow2)
			{
				if(parity == arr[i+j] || arr[i+j] == 'R') parity = '0';
				else parity = '1';
				j++;
			}
		}
		arr[pow2] = parity;

		pow2 = pow2 * 2;
	}
	
	printf("\nAfter Red,\n");
	HammingCode_printArr();
}

void HammingCode_Transmitter()
{
	printf("----------------------HC TCP/IP Transmitter-----------------------------\n");

	int error = ClientCreate(9009, 1, "");
	if(error == 1)
	{
		close(c_socket);
		printf("Connection Issue.\n");
	}
	else 
	{
		char bitarr[100];
		int bitarr_size = 0;

		int exit = 0;

		while(exit == 0)
		{
			printf("Enter bit array: ");
			scanf("%s", bitarr);

			bitarr_size = strlen(bitarr);

			printf("\nSizes: bit: %d\n", bitarr_size);
			printf("\nOriginal bit array: %s\n", bitarr);

			HammingCode_Generate(bitarr, bitarr_size);

			printf("\nSending message(%d): %s\n", arr_size, arr);

			strcat(arr, "\0");

			send(c_socket, arr, sizeof(arr), 0);
			printf("\nHC Array Sent.\n");

			char sent[] = "sent";
			send(c_socket, sent, sizeof(sent), 0);

			printf("Do you want to exit: ");
			scanf("%d", &exit);
		}
	}

	close(c_socket);

	printf("\n---------------------------------------------------------------------\n");	
}

// Sliding Window Protocol
void SlidingWindow_Receiver()
{
	printf("----------------------SlidingWindow Receiver-----------------------------\n");

	int ex = 0;

	while(ex == 0)
	{
		int port;
		printf("Enter Port: ");
		scanf("%d", &port);

		int window_size = 1;
		printf("Enter Window Size: ");
		scanf("%d", &window_size);

		int accepterror = 0;
		int error = ServerCreate(port);
		accepterror = AcceptNewClient();
		if(error == 1 || accepterror != 0)
		{
			close(s_server);
			close(s_socket);
			printf("Server Issue.\n");
		}
		else 
		{
			printf("\nServer Waiting...\n");

			char data[100];
			int index = 0;

			char ack[2];
			ack[0] = '1';
			ack[1] = '\0';

			char ack_temp[2];

			char buf[2];

			char exit[2];
			int exloop = 0;
			while(exloop == 0)
			{
				recv(s_server, exit, sizeof(exit), 0);
				if(exit[0] == '1')
				{
					exloop = 1;
					//continue;
				}
				else 
				{
					for(int i=0;i<window_size;i++)
					{
						recv(s_server, buf, sizeof(buf), 0);
						printf("Buf: %s\n", buf);
						data[index] = buf[0];
						index++;
					}
					
					
					for(int i=0;i<window_size;i++)
					{
						printf("Ack: ");
						scanf("%s", ack_temp);
						ack[0] = ack_temp[0];
						
						send(s_server, ack, sizeof(ack), 0);
						if(ack[0] == '0')
						{
							index = index - window_size + i;
							i = window_size;
						}
					}
					
				}
			}
			printf("Data: %s\n", data);
		}

		close(s_server);
		close(s_socket);

		printf("Do you want to exit: ");
		scanf("%d", &ex);
	}
	printf("\n---------------------------------------------------------------------\n");	
}

void SlidingWindow_Transmitter()
{
	printf("----------------------SlidingWindow Transmitter-----------------------------\n");

	int exit = 0;

	while(exit == 0)
	{
		char ipaddr[20];
		printf("Enter IP Address: ");
		scanf("%s", ipaddr);

		int port;
		printf("Enter Port: ");
		scanf("%d", &port);

		int window_size = 1;
		printf("Enter Window Size: ");
		scanf("%d", &window_size);

		int error = ClientCreate(port, 0, ipaddr);
		if(error == 1)
		{
			close(c_socket);
			printf("Connection Issue.\n");
		}
		else 
		{
			char data[100];
			printf("Enter data to send: ");
			scanf("%s", data);

			char ack[2];
			ack[0] = '1';
			ack[1] = '\0';

			char buf[2];
			buf[0] = '1';
			buf[1] = '\0';

			char exit[2];
			exit[0] = '0';
			exit[1] = '\0';

			int index = 0;
			while(index < strlen(data))
			{
				send(c_socket, exit, sizeof(exit), 0);
				for(int i=0;i<window_size;i++)
				{
					printf("Sending: %c\n", data[index + i]);
					buf[0] = data[index + i];
					send(c_socket, buf, sizeof(buf), 0);
				}
				int ack_check = -1;
				for(int i=0;i<window_size;i++)
				{
					recv(c_socket, ack, sizeof(ack), 0);
					printf("ACK: %s\n", ack);
					if(ack[0] == '0')
					{
						ack_check = i;
						i=window_size;
					}
				}
				if(ack_check == -1) index = index + window_size;
				else index = index + ack_check;
			}
			exit[0] = '1';
			send(c_socket, exit, sizeof(exit), 0);

			//close(c_socket);
		}

		printf("Do you want to exit: ");
		scanf("%d", &exit);

		if(exit != 0)
		{
			char exit_str[] = "/exit";
			send(c_socket, exit_str, sizeof(exit_str), 0);
			send(c_socket, exit_str, sizeof(exit_str), 0);
		}

		close(c_socket);
	}
	printf("\n---------------------------------------------------------------------\n");	
}

// Stop and Wait Protocol
void StopWait_Receiver()
{
	printf("----------------------Stop&Wait Receiver-----------------------------\n");

	int ex = 0;

	while(ex == 0)
	{
		int port;
		printf("Enter Port: ");
		scanf("%d", &port);

		int accepterror = 0;
		int error = ServerCreate(port);
		accepterror = AcceptNewClient();
		if(error == 1 || accepterror != 0)
		{
			close(s_server);
			close(s_socket);
			printf("Server Issue.\n");
		}
		else 
		{
			printf("\nServer Waiting...\n");

			char data[100];
			int index = 0;

			char ack[2];
			ack[0] = '1';
			ack[1] = '\0';

			char ack_temp[2];

			char buf[2];

			char exit[2];
			int exloop = 0;
			while(exloop == 0)
			{
				recv(s_server, exit, sizeof(exit), 0);
				if(exit[0] == '1')
				{
					exloop = 1;
					//continue;
				}
				else 
				{
					recv(s_server, buf, sizeof(buf), 0);
					printf("Buf: %s\n", buf);

					printf("Ack: ");
					scanf("%s", ack_temp);
					ack[0] = ack_temp[0];
					if(ack[0] == '1')
					{
						data[index] = buf[0];
						index++;
					}
					send(s_server, ack, sizeof(ack), 0);
				}
			}
			printf("Data: %s\n", data);
		}

		close(s_server);
		close(s_socket);

		printf("Do you want to exit: ");
		scanf("%d", &ex);
	}
	printf("\n---------------------------------------------------------------------\n");	
}

void StopWait_Transmitter()
{
	printf("----------------------Stop&Wait Transmitter-----------------------------\n");

	int exit = 0;

	while(exit == 0)
	{
		char ipaddr[20];
		printf("Enter IP Address: ");
		scanf("%s", ipaddr);

		int port;
		printf("Enter Port: ");
		scanf("%d", &port);

		int error = ClientCreate(port, 0, ipaddr);
		if(error == 1)
		{
			close(c_socket);
			printf("Connection Issue.\n");
		}
		else 
		{
			char data[100];
			printf("Enter data to send: ");
			scanf("%s", data);

			char ack[2];
			ack[0] = '1';
			ack[1] = '\0';

			char buf[2];
			buf[0] = '1';
			buf[1] = '\0';

			char exit[2];
			exit[0] = '0';
			exit[1] = '\0';

			int index = 0;
			while(index < strlen(data))
			{
				printf("Sending: %c\n", data[index]);
				buf[0] = data[index];
				send(c_socket, exit, sizeof(exit), 0);
				send(c_socket, buf, sizeof(buf), 0);
				recv(c_socket, ack, sizeof(ack), 0);
				printf("ACK: %s\n", ack);
				if(ack[0] == '1') index++;
			}
			exit[0] = '1';
			send(c_socket, exit, sizeof(exit), 0);

			//close(c_socket);
		}

		printf("Do you want to exit: ");
		scanf("%d", &exit);

		if(exit != 0)
		{
			char exit_str[] = "/exit";
			send(c_socket, exit_str, sizeof(exit_str), 0);
			send(c_socket, exit_str, sizeof(exit_str), 0);
		}

		close(c_socket);
	}
	printf("\n---------------------------------------------------------------------\n");	
}

// Routing Table
struct Device
{
	char device_name[100];
	char ip_addr[100];
	char port[20];
	int connected_to_this;
};

struct RoutingTable
{
	struct Device devices[4];
};

void RoutingTableInit(char devicenames[][100], char ipaddrs[][100], char subnetid[][100], char ports[][20], int no_of_devices, char this_device_name[], int connections[][100])
{
	int this_device_index = 0;
	for(int i=0;i<no_of_devices;i++)
	{
		if(strcmp(devicenames[i], this_device_name) == 0) this_device_index = i;
	}

	for(int i=0;i<no_of_devices;i++)
	{
		strcpy(rt.devices[i].device_name, devicenames[i]);
		strcpy(rt.devices[i].ip_addr, ipaddrs[i]);
		strcpy(rt.devices[i].subnetid, subnetid[i]);
		strcpy(rt.devices[i].port, ports[i]);
		if(connections[this_device_index][i] == 1 && connections[i][this_device_index] == 1) rt.devices[i].connected_to_this = 1;
		else rt.devices[i].connected_to_this = 0;
	}
}

int GetRoutingTableIndex(char device_name[], int no_of_devices)
{
	for(int i=0;i<no_of_devices;i++)
	{
		if(strcmp(rt.devices[i].device_name, device_name) == 0) return i;
	}
	return -1;
}

int no_of_bits(int no_of_devices)
{
	int bits = 0;
	while(no_of_devices > 0)
	{
		bits++;
		no_of_devices /= 2;
		if(no_of_devices == 1) break;
	}
	return bits;
}

char GetClassID(char ip[])
{
	char class;

	int classid = (ip[2]-48) + 10*(ip[1]-48) + 100*(ip[0]-48);
	if(classid >= 0 && classid <= 127) class = 'a';
	if(classid >= 128 && classid <= 191) class = 'b';
	if(classid >= 192 && classid <= 223) class = 'c';
	if(classid >= 224 && classid <= 239) class = 'd';
	if(classid >= 240 && classid <= 254) class = 'e';

	return class;
}

int GetIPPart(int bits)
{
	int ippart = 0;
	int inc = 128;
	while(bits > 0)
	{
		ippart += inc;
		inc /= 2;
		bits--;
	}
	return ippart;
}

int RoutingTableCreator()
{
	int no_of_devices = 4;
	char devicenames[/*no_of_devices*/][100] = {"A", "B", "C", "D"};
	char ipaddrs[/*no_of_devices*/][100] = {"127.0.0.1", "127.0.0.1", "127.0.0.1", "127.0.0.1"};
	char ports[/*no_of_devices*/][20] = {"9009", "9010", "9011", "9012"};
	int connections[/*no_of_devices*/][100] = {
													 {-1, 1, 0, 0},
													 {1, -1, 0, 1},
													 {0, 0, -1, 1},
													 {0, 1, 1, -1}
	};




	char this_device_name[100];
	printf("Enter this Device name: ");
	scanf("%s", this_device_name);

	RoutingTableInit(devicenames, ipaddrs, ports, no_of_devices, this_device_name, connections);

	int self_index = GetRoutingTableIndex(this_device_name, no_of_devices);

	printf("\n------------------------NODE %s---------------------------\n", this_device_name);
	printf("\nName: %s, IP: %s, Port: %s\n", this_device_name, rt.devices[self_index].ip_addr, rt.devices[self_index].port);

	//Create Server
	//int port = 9009;
	//printf("Enter port: ");
	//scanf("%d", &port);
	int errors = ServerCreate(atoi(rt.devices[self_index].port));
	if(errors == 1)
	{
		close(s_server);
		close(s_socket);
		return 0;
	}

	pthread_t tid;
	pthread_attr_t attr;
	pthread_attr_init(&attr);
	pthread_create(&tid, &attr, AcceptNewClient, NULL);

	//init vars
	int choice = 0;
	printf("Do you want to send(0/1): ");
	scanf("%d", &choice);

	if(choice == 1)
	{
		char text[500];
		char dest_devicename[100];

		printf("Enter Destination Device Name: ");
		scanf("%s", dest_devicename);
/*
		printf("Enter IP Address to send: ");
		scanf("%s", rt.ip_addr);
*/
		printf("Enter text to send: ");
		scanf("%s", text);

		int this_device_index = GetRoutingTableIndex(this_device_name, no_of_devices);
		int dest_device_index = GetRoutingTableIndex(dest_devicename, no_of_devices);

		if(this_device_index != -1 && dest_device_index != -1 && this_device_index != dest_device_index)
		{
			if(rt.devices[dest_device_index].connected_to_this == 1)
			{
				errors = ClientCreate(atoi(rt.devices[dest_device_index].port), rt.devices[dest_device_index].ip_addr);
				if(errors == 1)
				{
					printf("\nERROR in Connection to %s.\n", rt.devices[dest_device_index].device_name);
					close(c_socket);
					//return 0;
				}
				else
				{
					send(c_socket, rt.devices[this_device_index].device_name, sizeof(rt.devices[this_device_index].device_name), 0);
					send(c_socket, rt.devices[this_device_index].ip_addr, sizeof(rt.devices[this_device_index].ip_addr), 0);
					send(c_socket, rt.devices[this_device_index].port, sizeof(rt.devices[this_device_index].port), 0);
					send(c_socket, rt.devices[dest_device_index].device_name, sizeof(rt.devices[dest_device_index].device_name), 0);
					send(c_socket, rt.devices[dest_device_index].ip_addr, sizeof(rt.devices[dest_device_index].ip_addr), 0);
					send(c_socket, rt.devices[dest_device_index].port, sizeof(rt.devices[dest_device_index].port), 0);
					send(c_socket, text, sizeof(text), 0);
					close(c_socket);
				}
			}
			else
			{
				for(int i=0;i<no_of_devices;i++)
				{
					if(rt.devices[i].connected_to_this == 1)
					{
						errors = ClientCreate(atoi(rt.devices[i].port), rt.devices[i].ip_addr);
						if(errors == 1)
						{
							printf("\nERROR in Connection to %s.\n", rt.devices[i].device_name);
							close(c_socket);
							//return 0;
						}
						else
						{
							send(c_socket, rt.devices[this_device_index].device_name, sizeof(rt.devices[this_device_index].device_name), 0);
							send(c_socket, rt.devices[this_device_index].ip_addr, sizeof(rt.devices[this_device_index].ip_addr), 0);
							send(c_socket, rt.devices[this_device_index].port, sizeof(rt.devices[this_device_index].port), 0);
							send(c_socket, rt.devices[dest_device_index].device_name, sizeof(rt.devices[dest_device_index].device_name), 0);
							send(c_socket, rt.devices[dest_device_index].ip_addr, sizeof(rt.devices[dest_device_index].ip_addr), 0);
							send(c_socket, rt.devices[dest_device_index].port, sizeof(rt.devices[dest_device_index].port), 0);
							send(c_socket, text, sizeof(text), 0);
							close(c_socket);
						}
					}
				}
			}
		}
	}
	else
	{
		printf("\nWaiting for data......\n");

		pthread_join(tid, NULL);

		char src_devicename[100];
		char dest_devicename[100];
		char dest_ipaddr[100];
		char src_ipaddr[100];
		char dest_port[20];
		char src_port[20];
		char dest_text[500];

		recv(s_server, src_devicename, sizeof(src_devicename), 0);
		recv(s_server, src_ipaddr, sizeof(src_ipaddr), 0);
		recv(s_server, src_port, sizeof(src_port), 0);
		recv(s_server, dest_devicename, sizeof(dest_devicename), 0);
		recv(s_server, dest_ipaddr, sizeof(dest_ipaddr), 0);
		recv(s_server, dest_port, sizeof(dest_port), 0);
		recv(s_server, dest_text, sizeof(dest_text), 0);

		strcpy(src_ipaddr, inet_ntoa(other.sin_addr));

		// printf("\nConnection SRC: src_devicename: %s, src_ipaddr: %s, src_port: %s\n", src_devicename, src_ipaddr, src_port);
		// printf("\nConnection DEST: dest_devicename: %s, dest_ipaddr: %s, dest_port: %s\n", dest_devicename, dest_ipaddr, dest_port);
		// printf("\nConnection TEXT: %s\n", dest_text);

		if(strcmp(dest_devicename, this_device_name) == 0)
		{
			printf("Device %s with IP %s sent text: %s", src_devicename, dest_ipaddr, dest_text);
		}
		else
		{
			int this_device_index = GetRoutingTableIndex(this_device_name, no_of_devices);
			int dest_device_index = GetRoutingTableIndex(dest_devicename, no_of_devices);

			if(this_device_index != -1 && dest_device_index != -1 && this_device_index != dest_device_index)
			{
				if(rt.devices[dest_device_index].connected_to_this == 1)
				{
					errors = ClientCreate(atoi(dest_port), rt.devices[dest_device_index].ip_addr);
					if(errors == 1)
					{
						printf("\nERROR in Connection to %s.\n", dest_devicename);
						close(c_socket);
						//return 0;
					}
					else
					{
						send(c_socket, rt.devices[this_device_index].device_name, sizeof(rt.devices[this_device_index].device_name), 0);
						send(c_socket, rt.devices[this_device_index].ip_addr, sizeof(rt.devices[this_device_index].ip_addr), 0);
						send(c_socket, rt.devices[this_device_index].port, sizeof(rt.devices[this_device_index].port), 0);
						send(c_socket, dest_devicename, sizeof(dest_devicename), 0);
						send(c_socket, dest_ipaddr, sizeof(dest_ipaddr), 0);
						send(c_socket, dest_port, sizeof(dest_port), 0);
						send(c_socket, dest_text, sizeof(dest_text), 0);
						close(c_socket);
					}
				}
				else
				{
					for(int i=0;i<no_of_devices;i++)
					{
						if(rt.devices[i].connected_to_this == 1)
						{
							if(!(strcmp(rt.devices[i].device_name, src_devicename)) && !(strcmp(rt.devices[i].ip_addr, src_ipaddr)))
							{
								errors = ClientCreate(atoi(rt.devices[i].port), rt.devices[i].ip_addr);
								if(errors == 1)
								{
									printf("\nERROR in Connection to %s.\n", rt.devices[i].device_name);
									close(c_socket);
									//return 0;
								}
								else
								{
									send(c_socket, rt.devices[this_device_index].device_name, sizeof(rt.devices[this_device_index].device_name), 0);
									send(c_socket, rt.devices[this_device_index].ip_addr, sizeof(rt.devices[this_device_index].ip_addr), 0);
									send(c_socket, rt.devices[this_device_index].port, sizeof(rt.devices[this_device_index].port), 0);
									send(c_socket, dest_devicename, sizeof(dest_devicename), 0);
									send(c_socket, dest_ipaddr, sizeof(dest_ipaddr), 0);
									send(c_socket, dest_port, sizeof(dest_port), 0);
									send(c_socket, dest_text, sizeof(dest_text), 0);
									close(c_socket);
								}
							}
						}
					}
				}
			}
		}
	}
	printf("\n------------------------------------------------------------\n");
	return 0;
}

int RoutingTableCreator_WithSubnet()
{
	int no_of_devices = 4;
	int subnet_bits = no_of_bits(no_of_devices);

	int host_bits = 0;

	char devicenames[/*no_of_devices*/][100] = {"A", "B", "C", "D"};
	char ipaddrs[/*no_of_devices*/][100] = {"127.0.0.1", "127.0.0.1", "127.0.0.1", "127.0.0.1"};
	char subnetid[/*no_of_devices*/][100] = {"127.0.0.0", "127.64.0.0", "127.128.0.1", "127.192.0.1"};
	char ports[/*no_of_devices*/][20] = {"9009", "9010", "9011", "9012"};
	int connections[/*no_of_devices*/][100] = {
													 {-1, 1, 0, 0},
													 {1, -1, 0, 1},
													 {0, 0, -1, 1},
													 {0, 1, 1, -1}
	};

	char this_device_name[100];
	printf("Enter this Device name: ");
	scanf("%s", this_device_name);

	RoutingTableInit(devicenames, ipaddrs, subnetid, ports, no_of_devices, this_device_name, connections);

	int self_index = GetRoutingTableIndex(this_device_name, no_of_devices);

	printf("\n------------------------NODE %s---------------------------\n", this_device_name);
	printf("\nName: %s, IP: %s, Port: %s\n", this_device_name, rt.devices[self_index].ip_addr, rt.devices[self_index].port);

	//Create Server
	//int port = 9009;
	//printf("Enter port: ");
	//scanf("%d", &port);
	int errors = ServerCreate(atoi(rt.devices[self_index].port));
	if(errors == 1)
	{
		close(s_server);
		close(s_socket);
		return 0;
	}

	pthread_t tid;
	pthread_attr_t attr;
	pthread_attr_init(&attr);
	pthread_create(&tid, &attr, AcceptNewClient, NULL);

	//init vars
	int choice = 0;
	printf("Do you want to send(0/1): ");
	scanf("%d", &choice);

	if(choice == 1)
	{
		char text[500];
		char dest_deviceIP[100];
		char dest_devicename[100];

		printf("Enter Destination Device IP: ");
		scanf("%s", dest_deviceIP);

		char subnetmask[100];
		char class = GetClassID(dest_deviceIP);

		printf("\nCLASS: %c\n", class);
		printf("\nSUBNETBITS: %d\n", subnet_bits);

		if(class == 'a')
		{
			strcpy(subnetmask, "255.");
			if(subnet_bits <= 8)
			{
				char itoatemp[100];
				sprintf(itoatemp, "%d", GetIPPart(subnet_bits));
				strcat(subnetmask, itoatemp);
				strcat(subnetmask, ".0.0");
			}
			else if(subnet_bits <= 16)
			{
				char itoatemp[100];
				strcat(subnetmask, "255.");
				sprintf(itoatemp, "%d", GetIPPart(subnet_bits - 8));
				strcat(subnetmask, itoatemp);
				strcat(subnetmask, ".0");
			}
			else if(subnet_bits <= 24)
			{
				char itoatemp[100];
				strcat(subnetmask, "255.255.");
				sprintf(itoatemp, "%d", GetIPPart(subnet_bits - 16));
				strcat(subnetmask, itoatemp);
			}
		}
		else if(class == 'b')
		{
			strcpy(subnetmask, "255.255.");
			if(subnet_bits <= 8)
			{
				char itoatemp[100];
				sprintf(itoatemp, "%d", GetIPPart(subnet_bits));
				strcat(subnetmask, itoatemp);
				strcat(subnetmask, ".0");
			}
			else if(subnet_bits <= 16)
			{
				char itoatemp[100];
				strcat(subnetmask, "255.");
				sprintf(itoatemp, "%d", GetIPPart(subnet_bits - 8));
				strcat(subnetmask, itoatemp);
			}
		}
		else if(class == 'c')
		{
			strcpy(subnetmask, "255.255.255.");
			if(subnet_bits <= 8)
			{
				char itoatemp[100];
				sprintf(itoatemp, "%d", GetIPPart(subnet_bits));
				strcat(subnetmask, itoatemp);
			}
		}

		printf("\nSUBNETMASK: %s\n", subnetmask);

		int subnetid_val[4];
		for(int i=0;i<4;i++)
		{
			int temp = 0;
			int a = (dest_deviceIP[i*4 + 2]-48) + 10*(dest_deviceIP[i*4 + 1]-48) + 100*(dest_deviceIP[i*4 + 0]-48);
			int b = (subnetmask[i*4 + 2]-48) + 10*(subnetmask[i*4 + 1]-48) + 100*(subnetmask[i*4 + 0]-48);
			while(a > 0 || b > 0)
			{
				temp = 10*temp + (a%2 && b%2);
				if(a == 0) break;
				if(b == 0) break;
				a /= 2;
				b /= 2;
			}
			int temp2 = 0;
			while(temp > 0)
			{
				temp2 = 10*temp2 + temp%10;
				temp /= 10;
			}
			temp = temp2;
			int val = 1;
			while(temp > 0)
			{
				subnetid_val[i] += val*(temp%10);
				temp /= 10;
				if(temp == 0) break;
				val *= 2;
			}
		}
		char dest_subnetid[100];
		char subnettemp[100];
		sprintf(subnettemp, "%d", subnetid_val[0]);
		strcpy(dest_subnetid, subnettemp);
		strcat(dest_subnetid, ".");
		sprintf(subnettemp, "%d", subnetid_val[1]);
		strcat(dest_subnetid, subnettemp);
		strcat(dest_subnetid, ".");
		sprintf(subnettemp, "%d", subnetid_val[2]);
		strcat(dest_subnetid, subnettemp);
		strcat(dest_subnetid, ".");
		sprintf(subnettemp, "%d", subnetid_val[3]);
		strcat(dest_subnetid, subnettemp);

		printf("\nSUBNETID DEST: %s\n", dest_subnetid);

/*
		printf("Enter IP Address to send: ");
		scanf("%s", rt.ip_addr);
*/
		printf("Enter text to send: ");
		scanf("%s", text);

		int this_device_index = GetRoutingTableIndex(this_device_name, no_of_devices);
		int dest_device_index = -1;

		for(int i=0;i<no_of_devices;i++)
		{
			if(strcmp(rt.devices[i].subnetid, dest_subnetid) == 0) dest_device_index = i;
		}

		if(dest_device_index != -1) strcpy(dest_devicename, rt.devices[dest_device_index].device_name);

		if(this_device_index != -1 && dest_device_index != -1 && this_device_index != dest_device_index)
		{
			if(rt.devices[dest_device_index].connected_to_this == 1)
			{
				errors = ClientCreate(atoi(rt.devices[dest_device_index].port), rt.devices[dest_device_index].ip_addr);
				if(errors == 1)
				{
					printf("\nERROR in Connection to %s.\n", rt.devices[dest_device_index].device_name);
					close(c_socket);
					//return 0;
				}
				else
				{
					send(c_socket, rt.devices[this_device_index].device_name, sizeof(rt.devices[this_device_index].device_name), 0);
					send(c_socket, rt.devices[this_device_index].ip_addr, sizeof(rt.devices[this_device_index].ip_addr), 0);
					send(c_socket, rt.devices[this_device_index].port, sizeof(rt.devices[this_device_index].port), 0);
					send(c_socket, rt.devices[dest_device_index].device_name, sizeof(rt.devices[dest_device_index].device_name), 0);
					send(c_socket, rt.devices[dest_device_index].ip_addr, sizeof(rt.devices[dest_device_index].ip_addr), 0);
					send(c_socket, rt.devices[dest_device_index].port, sizeof(rt.devices[dest_device_index].port), 0);
					send(c_socket, text, sizeof(text), 0);
					close(c_socket);
				}
			}
			else
			{
				for(int i=0;i<no_of_devices;i++)
				{
					if(rt.devices[i].connected_to_this == 1)
					{
						errors = ClientCreate(atoi(rt.devices[i].port), rt.devices[i].ip_addr);
						if(errors == 1)
						{
							printf("\nERROR in Connection to %s.\n", rt.devices[i].device_name);
							close(c_socket);
							//return 0;
						}
						else
						{
							send(c_socket, rt.devices[this_device_index].device_name, sizeof(rt.devices[this_device_index].device_name), 0);
							send(c_socket, rt.devices[this_device_index].ip_addr, sizeof(rt.devices[this_device_index].ip_addr), 0);
							send(c_socket, rt.devices[this_device_index].port, sizeof(rt.devices[this_device_index].port), 0);
							send(c_socket, rt.devices[dest_device_index].device_name, sizeof(rt.devices[dest_device_index].device_name), 0);
							send(c_socket, rt.devices[dest_device_index].ip_addr, sizeof(rt.devices[dest_device_index].ip_addr), 0);
							send(c_socket, rt.devices[dest_device_index].port, sizeof(rt.devices[dest_device_index].port), 0);
							send(c_socket, text, sizeof(text), 0);
							close(c_socket);
						}
					}
				}
			}
		}
	}
	else
	{
		printf("\nWaiting for data......\n");

		pthread_join(tid, NULL);

		char src_devicename[100];
		char dest_devicename[100];
		char dest_ipaddr[100];
		char src_ipaddr[100];
		char dest_port[20];
		char src_port[20];
		char dest_text[500];

		recv(s_server, src_devicename, sizeof(src_devicename), 0);
		recv(s_server, src_ipaddr, sizeof(src_ipaddr), 0);
		recv(s_server, src_port, sizeof(src_port), 0);
		recv(s_server, dest_devicename, sizeof(dest_devicename), 0);
		recv(s_server, dest_ipaddr, sizeof(dest_ipaddr), 0);
		recv(s_server, dest_port, sizeof(dest_port), 0);
		recv(s_server, dest_text, sizeof(dest_text), 0);

		strcpy(src_ipaddr, inet_ntoa(other.sin_addr));

		// printf("\nConnection SRC: src_devicename: %s, src_ipaddr: %s, src_port: %s\n", src_devicename, src_ipaddr, src_port);
		// printf("\nConnection DEST: dest_devicename: %s, dest_ipaddr: %s, dest_port: %s\n", dest_devicename, dest_ipaddr, dest_port);
		// printf("\nConnection TEXT: %s\n", dest_text);

		if(strcmp(dest_devicename, this_device_name) == 0)
		{
			printf("Device %s with IP %s sent text: %s", src_devicename, dest_ipaddr, dest_text);
		}
		else
		{
			int this_device_index = GetRoutingTableIndex(this_device_name, no_of_devices);
			int dest_device_index = GetRoutingTableIndex(dest_devicename, no_of_devices);

			if(this_device_index != -1 && dest_device_index != -1 && this_device_index != dest_device_index)
			{
				if(rt.devices[dest_device_index].connected_to_this == 1)
				{
					errors = ClientCreate(atoi(dest_port), rt.devices[dest_device_index].ip_addr);
					if(errors == 1)
					{
						printf("\nERROR in Connection to %s.\n", dest_devicename);
						close(c_socket);
						//return 0;
					}
					else
					{
						send(c_socket, rt.devices[this_device_index].device_name, sizeof(rt.devices[this_device_index].device_name), 0);
						send(c_socket, rt.devices[this_device_index].ip_addr, sizeof(rt.devices[this_device_index].ip_addr), 0);
						send(c_socket, rt.devices[this_device_index].port, sizeof(rt.devices[this_device_index].port), 0);
						send(c_socket, dest_devicename, sizeof(dest_devicename), 0);
						send(c_socket, dest_ipaddr, sizeof(dest_ipaddr), 0);
						send(c_socket, dest_port, sizeof(dest_port), 0);
						send(c_socket, dest_text, sizeof(dest_text), 0);
						close(c_socket);
					}
				}
				else
				{
					for(int i=0;i<no_of_devices;i++)
					{
						if(rt.devices[i].connected_to_this == 1)
						{
							if(!(strcmp(rt.devices[i].device_name, src_devicename)) && !(strcmp(rt.devices[i].ip_addr, src_ipaddr)))
							{
								errors = ClientCreate(atoi(rt.devices[i].port), rt.devices[i].ip_addr);
								if(errors == 1)
								{
									printf("\nERROR in Connection to %s.\n", rt.devices[i].device_name);
									close(c_socket);
									//return 0;
								}
								else
								{
									send(c_socket, rt.devices[this_device_index].device_name, sizeof(rt.devices[this_device_index].device_name), 0);
									send(c_socket, rt.devices[this_device_index].ip_addr, sizeof(rt.devices[this_device_index].ip_addr), 0);
									send(c_socket, rt.devices[this_device_index].port, sizeof(rt.devices[this_device_index].port), 0);
									send(c_socket, dest_devicename, sizeof(dest_devicename), 0);
									send(c_socket, dest_ipaddr, sizeof(dest_ipaddr), 0);
									send(c_socket, dest_port, sizeof(dest_port), 0);
									send(c_socket, dest_text, sizeof(dest_text), 0);
									close(c_socket);
								}
							}
						}
					}
				}
			}
		}
	}
	printf("\n------------------------------------------------------------\n");
	return 0;
}