#include "warping_error.h"

int main(int argc, char* argv[]) {
	if (argc < 3 || argv[1] == "-h") {
		std::cerr << "Usage: warping_error.exe <groundtruth png> <user generated png>\n";	
	}

	std::string path_o = argv[1];
	std::string path_d = argv[2];
	cv::Mat img_o = cv::imread(path_o, 1);
	cv::Mat img_d = cv::imread(path_d, 1);
	//img_o.convertTo(img_o, CV_32SC1);
	//img_d.convertTo(img_d, CV_32SC1);

	Warping_error we;
	//std::vector<int> array_o, array_d, array_res;
	//array_o = std::vector<int>((int*)img_o.data, (int*)img_o.data + img_o.rows*img_o.cols);
	//array_d = std::vector<int>((int*)img_d.data, (int*)img_d.data + img_d.rows*img_d.cols);

	std::cout << we.compute_warping_error(img_o, img_d, false) << std::endl;
	//std::cout << we.compute_warping_error_python(img_o.rows, img_o.cols, array_o, array_d, array_res) << std::endl;
	//cv::Mat r(img_o.rows, img_o.cols, CV_32SC1, &array_res[0]);
	//r.convertTo(r, CV_8UC1);
	//cv::resize(r, r, cv::Size(), 5, 5);
	//cv::imshow("Window", r);
	//cv::waitKey();
	return 0;
}
