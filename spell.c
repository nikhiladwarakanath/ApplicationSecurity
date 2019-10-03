#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

char *trim(char *string_input);
void store_misspelled(char *misspelled);
char *substring(char *fullString, int posStart, int length);

bool load_dictionary(const char *dictionary_file, hashmap_t hashtable[])
{
    for (int i = 0; i < HASH_SIZE; i++)
    {
        hashtable[i] = NULL;
    }
    printf("inside load dictionary \n");
    FILE *fp = fopen(dictionary_file, "r");
    if (fp == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];
    while (fgets(word, sizeof(word), fp))
    {
        strtok(word, "\n");

        if (strlen(word) <= LENGTH)
        {
            //printf("%s:%d \n", word, strlen(word));
            node *new_node = (node *)malloc(sizeof(node));

            //new_node->next = NULL;

            strncpy(new_node->word, word, sizeof(word));
            int bucket = hash_function(word);
            if (hashtable[bucket] == NULL)
            {
                hashtable[bucket] = new_node;
                new_node->next = NULL;
            }
            else
            {
                new_node->next = hashtable[bucket];
                hashtable[bucket] = new_node;
            }
        }

        else
            continue;
    }
    printf("loaded \n");
    fclose(fp);
    return true;
}

int check_words(FILE *fp, hashmap_t hashtable[], char *misspelled[])
{

    int num_misspelled = 0, num_store = 0;
    //FILE *fpr = fopen(fp, "r");
    char LINE[100];
    

    while (fgets(LINE, 100, fp) != NULL)
    {
        
        //printf("%s \n", LINE);
        char *lineSplit = strtok(LINE, " ");
        //printf("%s:%d \n", lineSplit, strlen(lineSplit));
        if (strlen(lineSplit) <= LENGTH && lineSplit != NULL)
        {
            while (lineSplit != NULL)
            {
                //printf("%s \n", lineSplit);                
                char *trimmed = trim(lineSplit);
                //printf("trimming punctuation %s, %d \n", lineSplit, strlen(lineSplit));
                if (strlen(trimmed) > 0)
                {
                    if (!check_word(trimmed, hashtable))
                    {

                        //printf("Inside if \n");
                        if (num_store < 1000)
                        {
                            num_misspelled++;
                            //misspelled[num_store] =(char*) malloc(sizeof(char) * LENGTH +1 );
                            misspelled[num_store] = trimmed;
                            store_misspelled(trimmed);
                            num_store++;
                            //free(trimmed);
                        }
                        else{
                            free(trimmed);
                        }
                    }
                    else{
                        free(trimmed);
                    }
                    
                }
                else{
                    free(trimmed);
                }
                
                lineSplit = strtok(NULL, " ");
            }

            
        }
        else
        {
           free(lineSplit); //printf("NO");
        }
        
        //free(hashtable);

        //free(pos);
    }

    return num_misspelled;
}

bool check_word(const char *word, hashmap_t hashtable[])
{
    char lowerString[LENGTH + 1];
    int lengths = strlen(word);
    int i = 0;
    for (i = 0; i < lengths; i++)
    {
        lowerString[i] = tolower(word[i]);
    }
    lowerString[lengths] = '\0';
    //printf("inside checkword \n");
    int bucket = hash_function(lowerString);
    //printf("bucket value, %d \n", bucket);
    node *ptrToHash = hashtable[bucket];

    while (ptrToHash != NULL)
    {
        //printf(" word %d      ptrtohas %d ",strlen(word), strlen(ptrToHash-> word));
        if (strcmp(lowerString, ptrToHash->word) == 0)
        {
            //printf("success \n");
            return true;
        }
        else
            ptrToHash = ptrToHash->next;
    }
    //free(ptrToHash);
    //free(node);
    return false;
}

char *trim(char *string_input)
{
    int removeFromStart = 0;
    for (int i = 0; i < strlen(string_input); i++)
    {

        if (isalnum(string_input[i]))
        {

            removeFromStart = i;
            break;
        }
    }

    // Count end punctuation.
    int removeFromEnd = strlen(string_input)-1;
    for (int j = strlen(string_input) - 1; j >= 0; j--)
    {

        if (isalnum(string_input[j]))
        {

            removeFromEnd = j;
            break;
        }
    }
    char *finals;
    //finals = substring(string_input, removeFromStart, strlen(string_input));
    // // No characters were punctuation.
    // if (removeFromStart == 0 &&
    //     removeFromEnd == 0)
    // {
    //     return "";
    // }
    // // All characters were punctuation.
    if (removeFromStart == strlen(string_input) -1 &&
        removeFromEnd == 0)
    {
        return "";
    }
    // // Substring.

    //strncpy(finals, removeFromStart, removeFromEnd);
    finals = substring(string_input, removeFromStart, removeFromEnd);
    //strncpy(string_input, finals,sizeof(string_input));
    //free(finals);
    return finals;
}

char *substring(char *fullString, int posStart, int length)
{
    int i, c = 0;
    char *output = (char*) malloc(sizeof(char) * LENGTH +1 );
    for (i = posStart; i < length + 1; i++)
    {
        if (isspace(fullString[i]))
        {
            fullString[i] = '\0';
        }
        else

        {
            output[c] = fullString[i];
            c++;
        }
    }
    output[c] = '\0';
    //printf("\nsub string is %s\n", output);
    return output;
}

void store_misspelled(char *misspelled)
{
    FILE *fp;
    fp = fopen("misspelled.txt", "a");

    fputs(misspelled, fp);
    fputs("\n", fp);
    fclose(fp);
}
