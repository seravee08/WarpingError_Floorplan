#include "warping_error.h"

int main() {
	std::string path_o = "E:/Data2/ArcGIS/Floor_CAD/Dataset/warp_error_o.png";
	std::string path_d = "E:/Data2/ArcGIS/Floor_CAD/Dataset/warp_error_d.png";
	cv::Mat img_o = cv::imread(path_o, 1);
	cv::Mat img_d = cv::imread(path_d, 1);
	//img_o.convertTo(img_o, CV_32SC1);
	//img_d.convertTo(img_d, CV_32SC1);

	Warping_error we;
	//std::vector<int> array_o, array_d, array_res;
	//array_o = std::vector<int>((int*)img_o.data, (int*)img_o.data + img_o.rows*img_o.cols);
	//array_d = std::vector<int>((int*)img_d.data, (int*)img_d.data + img_d.rows*img_d.cols);

	std::cout << we.compute_warping_error(img_o, img_d, true) << std::endl;
	//std::cout << we.compute_warping_error_python(img_o.rows, img_o.cols, array_o, array_d, array_res) << std::endl;
	//cv::Mat r(img_o.rows, img_o.cols, CV_32SC1, &array_res[0]);
	//r.convertTo(r, CV_8UC1);
	//cv::resize(r, r, cv::Size(), 5, 5);
	//cv::imshow("Window", r);
	//cv::waitKey();

	system("pause");
	return 0;
}