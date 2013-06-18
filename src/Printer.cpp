#include "Printer.h"

#include <string>
#include <map>
#include <vector>
#include <iostream>

Printer::Printer(std::vector<std::map<std::string, int> >* combinations, std::map<int, std::string>* graphs, std::vector<std::string>* performanceCounters, std::string* sequenceIdParameter, std::map<std::string, std::map<int, std::vector<long long> > >* resultX, std::map<std::string, std::map<int, std::vector<long long> > >* resultY, std::string* unit) {

    _combinations = combinations;
    _graphs = graphs;
    _performanceCounters = performanceCounters;
    _sequenceIdParameter = sequenceIdParameter;

    _resultX = resultX;
    _resultY = resultY;

    _unit = unit;

}

Printer::Printer(std::vector<std::map<std::string, int> >* combinations) {

    _combinations = combinations;

}

void Printer::printResults() {

    std::cout << std::endl << "Results:" << std::endl << "#############" << std::endl;

    int graphId, positions;
    std::map<int, std::string>::iterator it;

    std::map<std::string, std::map<int, std::vector<long long> > > resultX = *_resultX;
    std::vector<std::string> performanceCounters = *_performanceCounters;
    std::vector<std::map<std::string, int> > combinations = *_combinations;


    for (size_t i = 0; i < _performanceCounters->size(); ++i) {

        for (it = _graphs->begin(); it != _graphs->end(); it++) {

            graphId = it->first;
            std::vector<long long> graphData;
            positions = resultX[performanceCounters[i]][graphId].size();
            
            for (int pos = 0; pos < positions; ++pos) {

                std::cout << resultX[performanceCounters[i]][graphId][pos] << " " << *_sequenceIdParameter << " -> " << this->getValue(graphId, performanceCounters[i], pos, combinations[pos]) << " " << *_unit << std::endl;
            }
        }
    }

}

long long Printer::getValue(size_t graph_id, std::string perf_ctr, size_t pos, std::map<std::string, int> parameters) {

    std::map<std::string, std::map<int, std::vector<long long> > > resultY = *_resultY;
    return resultY[perf_ctr][graph_id][pos];

}


void Printer::printCombinations() {

    std::vector<std::map<std::string, int> > combinations = *_combinations;

    std::map<std::string, int>::iterator it;

    for (size_t i = 0; i < combinations.size(); ++i) {

        for (it = combinations[i].begin(); it != combinations[i].end(); it++) {

            std::cout << it->first << " - " << it->second << std::endl;
        }

        std::cout << "-------" << std::endl;
    }

}

Printer::~Printer() { 

}