#include "warping_error.h"
#include "utility.h"
#include <fstream>
#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <nlohmann/json.hpp>

int main(int argc, char* argv[]) {

	bool cvt2_meters = true;
	Utility ut;
	std::string path_jsn1 = argv[1];
	std::string path_jsn2 = argv[2];
	std::vector<std::vector<std::vector<cv::Point2f>>> geometry1 = ut.read_geometry_JSON(path_jsn1, cvt2_meters);
	std::vector<std::vector<std::vector<cv::Point2f>>> geometry2 = ut.read_geometry_JSON(path_jsn2, cvt2_meters);
	std::vector<std::vector<std::vector<cv::Point2f>>> geometry_wrt1 = ut.cvt_geometry_format_obj2drw(geometry1);
	std::vector<std::vector<std::vector<cv::Point2f>>> geometry_wrt2 = ut.cvt_geometry_format_obj2drw(geometry2);
	std::vector<std::vector<float>> x1_1, y1_1, x2_1, y2_1;
	std::vector<std::vector<float>> x1_2, y1_2, x2_2, y2_2;
	ut.cvt_geometry2list(geometry_wrt1, x1_1, y1_1, x2_1, y2_1);
	ut.cvt_geometry2list(geometry_wrt2, x1_2, y1_2, x2_2, y2_2);
	cv::Mat img1 = ut.plot_layers(x1_1, y1_1, x2_1, y2_1, 5, -1);
	cv::Mat img2 = ut.plot_layers(x1_2, y1_2, x2_2, y2_2, 5, -1);
	cv::flip(img1, img1, 0);
	cv::flip(img2, img2, 0);
	const int rows1 = img1.rows;
	const int cols1 = img1.cols;
	const int rows2 = img2.rows;
	const int cols2 = img2.cols;
	// std::cout << "Result 1: height " << rows1 << " width " << cols1 << std::endl;
	// std::cout << "Result 2: height " << rows2 << " width " << cols2 << std::endl;
	if (rows1 > 640 && cols1 > 640) cv::resize(img1, img1, cv::Size(640, 640));
	if (rows2 > 640 && cols2 > 640) cv::resize(img2, img2, cv::Size(640, 640));

	Warping_error we;
	std::cout << we.compute_warping_error(img1, img2, false) << std::endl;

	// ===== Legacy Codes =====
	//std::string path_o = "E:/Data2/ArcGIS/Floor_CAD/Dataset/warp_error_o.png";
	//std::string path_d = "E:/Data2/ArcGIS/Floor_CAD/Dataset/warp_error_d.png";
	//cv::Mat img_o = cv::imread(path_o, 1);
	//cv::Mat img_d = cv::imread(path_d, 1);
	////img_o.convertTo(img_o, CV_32SC1);
	////img_d.convertTo(img_d, CV_32SC1);

	//Warping_error we;
	////std::vector<int> array_o, array_d, array_res;
	////array_o = std::vector<int>((int*)img_o.data, (int*)img_o.data + img_o.rows*img_o.cols);
	////array_d = std::vector<int>((int*)img_d.data, (int*)img_d.data + img_d.rows*img_d.cols);

	//std::cout << we.compute_warping_error(img_o, img_d, true) << std::endl;
	////std::cout << we.compute_warping_error_python(img_o.rows, img_o.cols, array_o, array_d, array_res) << std::endl;
	////cv::Mat r(img_o.rows, img_o.cols, CV_32SC1, &array_res[0]);
	////r.convertTo(r, CV_8UC1);
	////cv::resize(r, r, cv::Size(), 5, 5);
	////cv::imshow("Window", r);
	////cv::waitKey();
	// ============================

	system("pause");
	return 0;
}