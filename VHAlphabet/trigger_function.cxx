#include <TH1F.h>
#include <TFile.h>
double trigger_function(double htJet30=700) {
   double result;
   result = histo_efficiency->GetBinContent(htJet30);
   return result;    
   
   
}


#include <TH1F.h>
#include <TFile.h>
double trigger_function_lower(double htJet30=700) {
   double result;
   result = histo_efficiency_lower->GetBinContent(htJet30);
   return result;    
   
   
}


#include <TH1F.h>
#include <TFile.h>
double trigger_function_upper(double htJet30=700) {
   double result;
   result = histo_efficiency_upper->GetBinContent(htJet30);
   return result;    
   
   
}

