/*
 * High-Performance Retail Sales Data Analyzer in C++
 * Author: Data Analytics Project
 * Description: Ingests raw sales CSV data, parses transactions using std::fstream,
 *              computes aggregated metrics (Total Sales, Category Breakdown, AOV)
 *              with ultra-fast performance.
 *
 * Compilation Instructions:
 *   g++ -O3 -std=c++17 fast_retail_analyzer.cpp -o retail_analyzer
 *   ./retail_analyzer
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <iomanip>
#include <chrono>

struct Transaction {
    std::string transaction_id;
    std::string date;
    std::string customer_id;
    std::string gender;
    int age;
    std::string category;
    std::string product_name;
    int quantity;
    double price_per_unit;
    double total_amount;
    std::string payment_method;
    std::string location;
};

// Helper function to split CSV line handling basic commas
std::vector<std::string> parseCSVLine(const std::string& line) {
    std::vector<std::string> result;
    std::stringstream ss(line);
    std::string item;
    while (std::getline(ss, item, ',')) {
        result.push_back(item);
    }
    return result;
}

int main() {
    auto start_time = std::chrono::high_resolution_clock::now();

    std::string file_path = "../data/retail_sales_raw.csv";
    std::ifstream file(file_path);

    if (!file.is_open()) {
        file_path = "data/retail_sales_raw.csv"; // Fallback path check
        file.open(file_path);
    }

    if (!file.is_open()) {
        std::cerr << "Error: Could not open dataset at " << file_path << std::endl;
        std::cerr << "Please ensure data/retail_sales_raw.csv exists!" << std::endl;
        return 1;
    }

    std::string line;
    // Skip header line
    std::getline(file, line);

    std::vector<Transaction> transactions;
    double total_revenue = 0.0;
    int total_items_sold = 0;

    std::unordered_map<std::string, double> category_revenue;
    std::unordered_map<std::string, int> category_count;
    std::unordered_map<std::string, int> payment_counts;
    std::unordered_map<std::string, double> location_revenue;

    while (std::getline(file, line)) {
        if (line.empty()) continue;
        auto tokens = parseCSVLine(line);
        if (tokens.size() < 12) continue;

        Transaction t;
        t.transaction_id = tokens[0];
        t.date = tokens[1];
        t.customer_id = tokens[2];
        t.gender = tokens[3];
        t.age = std::stoi(tokens[4]);
        t.category = tokens[5];
        t.product_name = tokens[6];
        t.quantity = std::stoi(tokens[7]);
        t.price_per_unit = std::stod(tokens[8]);
        t.total_amount = std::stod(tokens[9]);
        t.payment_method = tokens[10];
        t.location = tokens[11];

        transactions.push_back(t);

        total_revenue += t.total_amount;
        total_items_sold += t.quantity;

        category_revenue[t.category] += t.total_amount;
        category_count[t.category] += t.quantity;
        payment_counts[t.payment_method]++;
        location_revenue[t.location] += t.total_amount;
    }

    file.close();

    auto end_time = std::chrono::high_resolution_clock::now();
    double execution_ms = std::chrono::duration<double, std::milli>(end_time - start_time).count();

    // Console output summary report
    std::cout << "=========================================================================\n";
    std::cout << "          FAST C++ RETAIL SALES DATA ANALYZER ENGINE RESULTS            \n";
    std::cout << "=========================================================================\n";
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Total Transactions Processed : " << transactions.size() << "\n";
    std::cout << "Total Units Sold             : " << total_items_sold << "\n";
    std::cout << "Total Generated Revenue      : $" << total_revenue << "\n";
    std::cout << "Average Order Value (AOV)    : $" << (total_revenue / transactions.size()) << "\n";
    std::cout << "Processing Time              : " << execution_ms << " ms\n";
    std::cout << "-------------------------------------------------------------------------\n";
    std::cout << " REVENUE & SALES BREAKDOWN BY PRODUCT CATEGORY:\n";
    std::cout << "-------------------------------------------------------------------------\n";

    std::string top_category = "";
    double max_cat_rev = 0.0;

    for (const auto& [cat, rev] : category_revenue) {
        std::cout << "  - " << std::left << std::setw(20) << cat 
                  << ": $" << std::right << std::setw(10) << rev 
                  << " (" << category_count[cat] << " units)\n";
        if (rev > max_cat_rev) {
            max_cat_rev = rev;
            top_category = cat;
        }
    }

    std::cout << "-------------------------------------------------------------------------\n";
    std::cout << " Top Performing Category     : " << top_category << " ($" << max_cat_rev << ")\n";
    std::cout << "-------------------------------------------------------------------------\n";
    std::cout << " REVENUE BY STORE LOCATION:\n";
    std::cout << "-------------------------------------------------------------------------\n";
    for (const auto& [loc, rev] : location_revenue) {
        std::cout << "  - Location: " << std::left << std::setw(10) << loc 
                  << " Revenue: $" << rev << "\n";
    }

    std::cout << "=========================================================================\n";

    return 0;
}
